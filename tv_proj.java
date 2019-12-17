package tv_pro;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringReader;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.apache.commons.collections.list.LazyList;
import org.eclipse.rdf4j.RDF4J;
import org.eclipse.rdf4j.model.IRI;
import org.eclipse.rdf4j.model.Literal;
//import org.eclipse.rdf4j.model.Model;
import org.eclipse.rdf4j.model.Model;
import org.eclipse.rdf4j.model.Statement;
import org.eclipse.rdf4j.model.URI;
import org.eclipse.rdf4j.model.Value;
import org.eclipse.rdf4j.model.ValueFactory;
import org.eclipse.rdf4j.model.impl.LinkedHashModel;
import org.eclipse.rdf4j.model.impl.SimpleValueFactory;
import org.eclipse.rdf4j.model.util.ModelBuilder;
import org.eclipse.rdf4j.model.vocabulary.FOAF;
import org.eclipse.rdf4j.model.vocabulary.RDF;
import org.eclipse.rdf4j.model.vocabulary.RDFS;
import org.eclipse.rdf4j.query.BindingSet;
import org.eclipse.rdf4j.query.QueryLanguage;
import org.eclipse.rdf4j.query.QueryResults;
import org.eclipse.rdf4j.query.TupleQuery;
import org.eclipse.rdf4j.query.TupleQueryResult;
import org.eclipse.rdf4j.query.resultio.text.csv.SPARQLResultsCSVWriter;
import org.eclipse.rdf4j.repository.Repository;
import org.eclipse.rdf4j.repository.RepositoryConnection;
import org.eclipse.rdf4j.repository.RepositoryException;
import org.eclipse.rdf4j.repository.RepositoryResult;
import org.eclipse.rdf4j.repository.sail.SailRepository;
import org.eclipse.rdf4j.repository.sail.SailRepositoryConnection;
import org.eclipse.rdf4j.repository.util.Repositories;
import org.eclipse.rdf4j.rio.RDFFormat;
import org.eclipse.rdf4j.rio.Rio;
import org.eclipse.rdf4j.sail.memory.MemoryStore;
import com.opencsv.CSVReader;
import org.eclipse.rdf4j.repository.Repository;
import org.eclipse.rdf4j.sail.nativerdf.NativeStore;
public class tv_proj 
{
	Repository repos = new SailRepository(new MemoryStore());
	public void mapping() throws IOException
	{
	 String[] mapping;
	 File file=new File("C:\\Users\\shubhangi\\Desktop\\capstone\\abc.rdf"); 
	 FileWriter filewriter = new FileWriter(file);
	 FileReader map = new FileReader("C:\\Users\\shubhangi\\Desktop\\capstone\\relations1.csv");
	 CSVReader c = new CSVReader(map); 
	 mapping = c.readNext();
	 int col1=4;
	 int col2=5;           
	 int count=0;
	 Repository repos = new SailRepository(new MemoryStore());
	 repos.initialize();	
	 String ns = "http://project.iiitd/";
	 ValueFactory f = repos.getValueFactory();
	// RepositoryConnection conn =repos.getConnection();
//	 String relatn=mapping[1];
//	System.out.print(relatn);
	 while ((mapping = c.readNext()) != null)
	{
		String filepath=mapping[3];
		//System.out.println(filepath);
		String Subject=mapping[col1];
		String object=mapping[col2];
		String[] rec;
		String relatn=mapping[1];
		//System.out.print(relatn+"\n");
		FileReader map1 = new FileReader(filepath);
		CSVReader csv = new CSVReader(map1); 
	   // rec = csv.readNext();
	    
	    while ((rec = csv.readNext()) != null)
	    {
	    	ModelBuilder build= new ModelBuilder();
		    //Model model=build.build();
	    	//build.setNamespace("ex", ns);
	    	int sub_col=Integer.parseInt(Subject);
	    	System.out.println(rec[col1]);
	    	//System.out.println(rec[col2]);
	    	int obj_col=Integer.parseInt(object);
	    	IRI sub=f.createIRI(ns,rec[sub_col]);
	    	IRI r=f.createIRI(ns,relatn);
	    	//String sub=rec[sub_col];
	    	//String r=relatn;
	    	Literal obj=f.createLiteral(rec[obj_col]);
	    	//System.out.println(sub);
			System.out.println(obj);
	    	 try(RepositoryConnection conn=repos.getConnection())
			    {
			    System.out.println(filepath);
	    		 Model model = build.build();
	    		 build=new ModelBuilder();
			    		//build.subject("ex:"+sub).add("ex:"+r,"ex:"+obj+" ");
			    		model.add(sub,r, obj);
			    		count=count+1;
			    		System.out.println(count);
			    		//model.add(sub, r, obj);
			 			Rio.write(model, filewriter, RDFFormat.TURTLE);
			 			Rio.write(model, System.out, RDFFormat.TURTLE);
			 			conn.add(model);
			    //m=build.build();
			    }
	    	 finally
	    	 {
	    		// System.out.println("hi");
	    	 }
	    	
	    }
	    	
	    }
	 try (RepositoryConnection conn3 = repos.getConnection())
	  {
    	 //RepositoryConnection conn3 = repos.getConnection();
		
    	 // String query = "select  Distinct ?s ?p1 ?p2 ?o1 ?o2  where {?s ?p1 ?o1;?p2 ?o2;?p1!=?p2.} limit 10";
    	  //String q="select  ?tw <http:\\project.iiitd\\chossesTo> ?Role WHERE {?Tw <http:\\project.iiitd\\chossesTo> ?Role} LIMIT 10 "; 
    	  String q1="prefix : <http://project.iiitd/>  select ?m ?p1 ?p2  ?o1 ?o2  WHERE {?m :consistsOf ?o1.?m :hasScreenSize ?o2} LIMIT 10";
//    	  String q2="prefix : <http://sweb_project.iiitd/>  select ?m ?p1 ?p2 ?o1 ?o2  WHERE {?m :playedBy ?o1. ?o1 :playRoles ?o2} LIMIT 10";
//    	  String q4="prefix : <http://sweb_project.iiitd/>  select ?m  ?p1 ?p2 ?p3 ?o1 ?o2 ?batsman  WHERE{?m :playedBy ?o1. ?m :bowledBy ?o2.?batsman :strikes ?o2} LIMIT 10";
//    	  String q5="prefix : <http://sweb_project.iiitd/>  select ?m  ?p1 ?p2 ?p3  ?o1 ?o2   WHERE {?m :playDate ?o1. ?o12 :locatedIn ?o3. ?o2 :usedOnDate ?o1} LIMIT 100";
    	  //String q2="SELECT DISTINCT ?s  ?Match ?Location ?City WHERE { ?s <http://www.w3.org/2000/01/rdf-schema#hasID> ?RestaurantID .?RestaurantID <http://www.w3.org/2000/01/rdf-schema#hasLocation> ?Location . ?Location <http://www.w3.org/2000/01/rdf-schema#hasCity> ?City} LIMIT 100
    	 //String queryString="SELECT ?s  ?Bat ?Ground WHERE { ?s <http://sweb_project.iiitd/chossesTo> ?Bat . <http://sweb_project.iiitd/playedAt> ?Ground } LIMIT 100";
    	 //String query = "select (count (*) AS ?cnt) where {?s ?p ?o}";
    	
    	 //List<BindingSet> results = Repositories.tupleQuery(repos,"\"select (count (*) AS ?cnt) where {?s ?p ?o}", r -> QueryResults.asList(r));
		  TupleQuery t=conn3.prepareTupleQuery(QueryLanguage.SPARQL,q1);
		  TupleQueryResult res1 = t.evaluate();
		  //System.out.println("hell");
			  //Value vx = null,vy=null;
			  List<String> bindingNames = res1.getBindingNames();
			  List<BindingSet> rl = null;
			  int te=0;
			  BindingSet bset;
			  //Value firstValue;
			  while(res1.hasNext())
			  {
				  //System.out.println("hell");
				  bset=res1.next();
				  //vx=bset.getValue("count");
				  Value  temp= bset.getValue("0");
				  
				  //System.out.println(te);
				  te=te+1;
				 //System.out.print("\t"+temp);
				  try (TupleQueryResult result = t.evaluate()) {
					   rl = QueryResults.asList(result);
					}
				 
			  }
			 //System.out.println("count1:"+te);
			System.out.println("$:"+rl.get(0));
			 // List<String> bindingNames = res1.getBindingNames();
			 
			  
	  }
	  finally
    	 {
    		 //System.out.println(count);
    	 }
	//System.out.println("count"+count1);
	//System.out.println(count);
	 
	 
}
	public static void main (String[] args) throws IOException
	{
		tv_proj m=new tv_proj();
		m.mapping();
		//m.query_map();
		//m.loadTriples();
	}
}

