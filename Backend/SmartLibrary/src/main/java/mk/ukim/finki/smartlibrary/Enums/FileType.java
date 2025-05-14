package mk.ukim.finki.smartlibrary.Enums;

public enum FileType {
    PDF,
    DOCX,
    CSV,
    TXT;

    public static FileType fromFileName(String fileName) {
        if (fileName.endsWith(".pdf")) {
            return PDF;
        } else if (fileName.endsWith(".docx")) {
            return DOCX;
        } else if (fileName.endsWith(".csv")) {
            return CSV;
        } else if (fileName.endsWith(".txt")) {
            return TXT;
        }
        throw new IllegalArgumentException("Unsupported file type: " + fileName);
    }
}
