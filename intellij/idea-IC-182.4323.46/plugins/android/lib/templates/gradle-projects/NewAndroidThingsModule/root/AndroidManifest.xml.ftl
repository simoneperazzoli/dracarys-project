<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="${packageName}"
    <#if !isLibraryProject>/</#if>><#if isLibraryProject>
    <application android:allowBackup="true"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <uses-library android:name="com.google.android.things"/>
    </application>
</manifest></#if>
