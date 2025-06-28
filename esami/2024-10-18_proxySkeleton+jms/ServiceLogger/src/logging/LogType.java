package logging;

public enum LogType {
    DEBUG(0),
    INFO(1),
    ERROR(2);

    private final int intValue;

    private LogType(int intValue) {
        this.intValue = intValue;
    }

    public int getIntValue() {
        return intValue;
    }

    public static LogType fromIntValue(int intValue) {
        LogType[] tipi = LogType.values();
        for (LogType logType : tipi) {
            if (logType.intValue == intValue)
                return logType;
        }
        return null;
    }

}
