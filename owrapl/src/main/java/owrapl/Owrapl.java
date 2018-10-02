package owrapl;

import java.io.File;

import org.semanticweb.owlapi.model.OWLException;

public class Owrapl {
    // Yes, I'm a pokemon trainer and I gotta catch'em all.
    public static void main(String[] args) throws OWLException {
        if (args.length == 0) {
            showUsage();
            return;
        }

        try {
            var input = args[0];
            var reader = OwlReader.fromFile(input);
            // reader = OwlReader.fromIRI("https://protege.stanford.edu/ontologies/pizza/pizza.owl");

            System.out.println("----------------------------------------\n\n");

            reader.infer();

            System.out.println("Prefix: " + reader.prefix());

            System.out.println(
                "Consistent? " + (reader.consistent() ? "Yes" : "No")
            );

            var subperson = reader.subclasses("Person");
            System.out.printf(
                "Subclasses of Person: %s (empty: %b)\n", subperson, subperson.isEmpty()
            );

            reader.save(System.out);

            System.out.println("\n\n----------------------------------------");
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
        System.out.printf(
            "Usage: %s <input owl file>" +
            "\n", executable
        );
    }
}
