package owrapl;

public final class Exceptions {
    private Exceptions() {}

    public static class CreationError extends RuntimeException {
        private static final long serialVersionUID = 1889786284600359726L;

        public CreationError(String message) {
            super("Failed to create ontology: " + message);
        }
    }

    public static class FileNotFound extends RuntimeException {
        private static final long serialVersionUID = 4073451917253199970L;

        public FileNotFound(String filename) {
            super("File not found: " + filename);
        }
    }

    public static class FailedToSave extends RuntimeException {
        private static final long serialVersionUID = -6214067735912386758L;

        public FailedToSave(String message) {
            super("Failed to save ontology: " + message);
        }
    }
}
