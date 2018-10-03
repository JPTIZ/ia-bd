package owrapl;

import java.io.File;
import java.io.OutputStream;

import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.formats.FunctionalSyntaxDocumentFormat;
import org.semanticweb.owlapi.io.OWLOntologyInputSourceException;
import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLNamedIndividual;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.model.OWLOntologyStorageException;
import org.semanticweb.owlapi.reasoner.NodeSet;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;
import org.semanticweb.owlapi.reasoner.structural.StructuralReasonerFactory;
import org.semanticweb.owlapi.util.InferredOntologyGenerator;

public class OwlReader {
    private OwlReader() {
        ontology = newOntology();
        reasoner = reasonerFactory.createReasoner(ontology);
    }

    public static OwlReader fromFile(String filename) {
        var reader = new OwlReader();

        reader.ontology = reader.ontologyFromFile(filename);

        return reader;
    }

    public void infer() {
        var inferred = new InferredOntologyGenerator(reasoner);

        inferred.fillOntology(
            manager.getOWLDataFactory(),
            ontology
        );
    }

    public String prefix() {
        return ontology.getOntologyID().getOntologyIRI().get().toString();
    }

    public boolean consistent() {
        reasoner.precomputeInferences();

        return reasoner.isConsistent();
    }

    public NodeSet<OWLClass> subclasses(String root) {
        var dataFactory = manager.getOWLDataFactory();
        var rootClass = dataFactory.getOWLClass(
            IRI.create(prefix() + "#" + root)
        );
        System.out.printf("Looking for subclasses of %s\n", prefix() + "#" + root);
        return reasoner.getSubClasses(rootClass, true);
    }

    public NodeSet<OWLNamedIndividual> individualsFromClass(String classname) {
        var classiri = IRI.create(classname); //IRI.create(prefix() + "#" + classname);

        System.out.println("Looking for individuals from class " + classiri);

        var dataFactory = manager.getOWLDataFactory();
        var _class = dataFactory.getOWLClass(classiri);
        return reasoner.getInstances(_class, false);
    }

    public void save(OutputStream stream) {
        try {
            ontology.saveOntology(
                new FunctionalSyntaxDocumentFormat(),
                System.out
            );
        } catch (OWLOntologyStorageException e) {
            throw new Exceptions.FailedToSave(e.getMessage());
        }
    }

    private OWLOntology ontologyFromFile(String filename) {
        var file = new File(filename);
        try {
            return manager.loadOntologyFromOntologyDocument(file);
        } catch (OWLOntologyCreationException e) {
            throw new Exceptions.CreationError(e.getMessage());
        } catch (OWLOntologyInputSourceException e) {
            throw new Exceptions.FileNotFound(filename);
        }
    }

    /*
    private OWLOntology ontologyFromIRI(String iriString) {
        var iri = IRI.create(iriString);

        return manager.loadOntologyFromOntologyDocument
    }
    */

    private OWLOntology newOntology() {
        try {
            return manager.createOntology();
        } catch (OWLOntologyCreationException e) {
            throw new Exceptions.CreationError(e.getMessage());
        }
    }

    private OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
    private OWLReasonerFactory reasonerFactory =
        new StructuralReasonerFactory();

    private OWLOntology ontology;
    private OWLReasoner reasoner;
}
