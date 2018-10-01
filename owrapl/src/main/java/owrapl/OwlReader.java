package owrapl;

import java.io.File;

import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.formats.FunctionalSyntaxDocumentFormat;
import org.semanticweb.owlapi.io.OWLOntologyInputSourceException;
import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLException;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyManager;

public class OwlReader {
    public OWLOntology ontologyFromFile(String filename) {
        var file = new File(filename);
        try {
            return manager.loadOntologyFromOntologyDocument(file);
        } catch (OWLOntologyCreationException e) {
            throw new Exceptions.CreationError();
        } catch (OWLOntologyInputSourceException e) {
            throw new Exceptions.FileNotFound(filename);
        }
    }

    OWLOntologyManager manager = OWLManager.createOWLOntologyManager();

    public static void showUsage() {
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

    // Yes, I'm a pokemon trainer and I gotta catch'em all.
    public static void main(String[] args) throws OWLException {
        if (args.length == 0) {
            showUsage();
            return;
        }

        try {
            var input = args[0];
            var reader = new OwlReader();
            var ontology = reader.ontologyFromFile(input);
            ontology.saveOntology(new FunctionalSyntaxDocumentFormat(), System.out);
        } catch (Exception e) {
            System.err.println(
                "----------------------------------------\n" +
                "[ERROR] " + e.getMessage() + "\n" +
                "----------------------------------------"
            );
        }
    }
}
