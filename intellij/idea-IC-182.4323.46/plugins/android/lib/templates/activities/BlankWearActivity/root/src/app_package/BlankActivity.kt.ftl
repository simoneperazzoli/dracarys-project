package ${escapeKotlinIdentifiers(packageName)}

import android.os.Bundle
import android.support.wearable.activity.WearableActivity

class ${activityClass} : WearableActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.${layoutName})

        // Enables Always-on
        setAmbientEnabled()
    }
}
