# Bibliotecas
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.dockarea import *
from kafka import KafkaProducer
import pyqtgraph as pg
import serial
import datetime
import re
import json

# Variáveis de configuração
producer = KafkaProducer(bootstrap_servers='localhost:9092')
initial_date_experiment = datetime.datetime('ano', 'mês', 'dia', 'hora', 'minuto') #inserir valores
path_to_output_data = "./"
time_monitoring = 0.1 # in seconds
time_saving = 0.1 # in seconds
size_graph = 1000 # in seconds

# Conecção com a Porta Serial
ser = serial.Serial('/dev/ttyACM1', 9600)

# Iniciando QtApp 
app = QtGui.QApplication([]) 
win = QtGui.QMainWindow()
win.setWindowTitle("Realtime plot DracarySP") 
area = DockArea()
win.setCentralWidget(area)
win.resize(1000,500)
dock_options = Dock("Options", size=(1, 1))
dock_plot = Dock("Plot", size=(500,200))
area.addDock(dock_plot, 'top')
area.addDock(dock_options, 'bottom')
widget_plot = pg.GraphicsWindow(title="Realtime plot DracarySP") 
p = widget_plot.addPlot(title="MDC Voltage") 
p.setLabel('left', "Voltage", units='mV')
p.setLabel('bottom', "Time", units='m')
dock_plot.addWidget(widget_plot)
curve = p.plot(pen='w') 
windowWidth = int(size_graph/time_monitoring)  
Xm = random.random((1,windowWidth))[0]  
Xm = linspace(0,0,num=len(Xm))
quantity_save = time_saving/time_monitoring
number_save = 0
ptr = -windowWidth 
win.show()

# Realtime data plot. 
def update(times, datas_file):
    global curve, p, ptr, Xm, number_save, quantity_save 
    diference_time = times[1] - times[0]
    if diference_time.total_seconds() >= time_monitoring: # time in seconds
        Xm[:-1] = Xm[1:]  
        try:
            value = ser.readline()
            value = float(re.findall("\d+\.\d+", value)[0])
        except:
            times[1] = datetime.datetime.now()
            QtGui.QApplication.processEvents() 
            return times
        Xm[-1] = value 
        ptr += 1 
        curve.setData(Xm) 
        curve.setPos(ptr,0)
        if number_save >= quantity_save:
            seconds_in_one_day = 86400.0
            timestamp_seconds = datetime.datetime.now() - initial_date_experiment
            timestamp_days_fraction = timestamp_seconds.total_seconds()/seconds_in_one_day 
            datas_file.write(str(timestamp_days_fraction) + ", " + str(value) + "," + "\n")
            number_save = 0
            print("Tempo: %s - Tensão: %s  " % (str(timestamp_days_fraction), str(value)))
            message_dict = {'timestamp': datetime.datetime.now().isoformat(), 'voltage': value}
            producer.send('test', json.dumps(message_dict))
        else:
            number_save += 1
        times[0] = datetime.datetime.now()
        times[1] = times[0]
    times[1] = datetime.datetime.now()
    QtGui.QApplication.processEvents() # you MUST process the plot now
    return times
widget_options = pg.LayoutWidget()
start_stop_button = QtGui.QPushButton('Start')
start_stop_button.setCheckable(True)
times = [datetime.datetime.now(), datetime.datetime.now()]
datas_file = None
update(times, datas_file)
def save():
    if start_stop_button.isChecked():
        start_stop_button.setText('Stop')
        date_file_name = initial_date_experiment.strftime("%d-%m-%Y-%H.%M.%S")
        name_file_output = path_to_output_data + "voltage_" + date_file_name + ".csv" 
        try:
            datas_file = open(name_file_output, "a")
        except:
            datas_file = open(name_file_output, "w")
        times = [datetime.datetime.now(), datetime.datetime.now()]
        while start_stop_button.isChecked() == True:
            times = update(times, datas_file)
        
        # start/stop operation
        start_stop_button.setText('Start')
        datas_file.close()
start_stop_button.clicked.connect(save)
widget_options.addWidget(start_stop_button, row=0, col=0)
dock_options.addWidget(widget_options)

### MAIN PROGRAM 
if __name__ == '__main__':
    pg.QtGui.QApplication.exec_() 


