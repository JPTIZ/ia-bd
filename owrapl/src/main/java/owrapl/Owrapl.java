package owrapl;

import static java.lang.System.out;

import java.io.File;
import java.io.PrintStream;
import java.io.OutputStream;

import org.semanticweb.owlapi.model.OWLException;

public class Owrapl {
    // Yes, I'm a pokemon trainer and I gotta catch'em all.
    public static void main(String[] args) throws OWLException {
        if (args.length == 0) {
            showUsage();
            return;
        }
        var input = args[0];

        try {
            printf("Loading %s...", input);
            disableErr();
            var reader = OwlReader.fromFile(input);
            enableErr();
            println("Done.");

            println("----------------------------------------\n\n");

            // reader.infer();

            println("Prefix: " + reader.prefix());

            println(
                "Consistent? " + (reader.consistent() ? "Yes" : "No")
            );

            var subperson = reader.subclasses("Person");
            printf(
                "Subclasses of Person: %s (empty: %b)\n", subperson, subperson.isEmpty()
            );

            var langs = reader.individualsFromClass("<http://webprotege.stanford.edu/RDmsQnYD1AMUV6qXn98JI1z>");
            printf("Languages: ");
            for (var lang: langs) {
                println(lang);
            }

            // reader.save(System.out);

            println("\n\n----------------------------------------");
        } catch (Exception e) {
            System.err.println(
                "----------------------------------------\n" +
                "[ERROR] " + e.getMessage() + "\n" +
                "----------------------------------------"
            );
        }
    }

    private static void showUsage() {
        var executable = "OwlReader";
        try {
            executable = new File(
                OwlReader.class
                    .getProtectionDomain()
                    .getCodeSource()
                    .getLocation()
                    .toURI()
                    .getPath()
                ).toString();
        } catch (Exception e) {}
        printf(
            "Usage: %s <input owl file>" +
            "\n", executable
        );
    }

    private static void printf(String format, Object... args) {
        out.printf(format, args);
    }

    private static <T> void println(T obj) {
        out.println(obj);
    }

    private static void println() {
        out.println();
    }

    private static void disableErr() {
        err = System.err;
        System.setErr(new PrintStream(new OutputStream() {
            public void write(int b) {}
        }));
    }

    private static void enableErr() {
        System.setErr(err);
    }

    private static PrintStream err = System.err;
}
