/** Class for CS555 Project 2 - GEMDoc file Reader
    @author Deborah Harrington
    */
import java.io.*;
import java.util.*;

public class GemDoc {
     
     // Variables
     /** HashMap for defining Valid Tag/Level info */
     private HashMap<String, String> validTags;

     /** HashMap for exceiption Tags/Level info */
     private HashMap<String, String> validExTags;

     /** nested class for processing a line read from an input file */
     private class GemDocLine {

	 // Variables
	 /** line read in */
         private String line;

	 /** split out tag */
         private String gTag;

	 /** split out arguments */
         private String gArg;

	 /** split out level */
         private String gLevel;

	 /** validity indicator of the tag/level */
	 private String validTag;
	 
         // Constructors
         /** constructor: initializes variables
             @param line input line
          */
         private GemDocLine(String line ) {
              if (line!=null && line.length() >= 1)
                    this.line=line;
	      else
                    this.line="";

		    this.gTag="";
		    this.gArg="";
		    this.gLevel="";
		    this.validTag="N";
         }
	 
         // Methods
         /** get_level - returns the parsed level
             @return level
          */
         private String get_level() {
             return gLevel;
         }

         /** get_tag - returns the parsed tag
             @return tag
          */
         private String get_tag() {
             return gTag;
         }

         /** get_args - returns the parsed arguments 
             @return arguments 
          */
         private String get_args() {
             return gArg;
         }
	 
         /** get_validity - return the Validity
             @return validity
          */
         private String get_validity() {
             return validTag;
         }

         /** parse_line - parses the input line
             @return none
          */
         private void parse_line() {
	     // don't do anything if the line is all blank - should never be null since is initialized to blank
	     if (line.trim()=="")
		return;

	     // grab the first parameter - delimetered by space- this is the LEVEL
     	     gLevel=line.substring(0, line.indexOf(" "));

	     // Remove the first parameter
     	     String sub_line = line.substring(line.indexOf(" "), line.length()).trim();
     
     	     // default the TAG to to the rest of the line (e.g. there are no arguments
	     // default the ARGUMENTS to blank
     	     gTag=sub_line;
     	     gArg="";

	     // if there is a space in the sub line - e.g. match from start to end of line at least one space....
	     // then need to split the TAG from the rest of the line
	     // and the remainder of the line will be arguments
     	     if (gTag.matches(".*\\s+.*"))
     	     {
		 // split the line to the space delimeter to get the TAG
     	         gTag=sub_line.substring(0, sub_line.indexOf(" "));

		 // All the rest are arguments
     		 gArg= sub_line.substring(sub_line.indexOf(" "), sub_line.length()).trim();
     	     }
     
	     // check if the tag is a valid Tag for the given TAG and LEVEL
	     // Treating the TAG as case sensitive - so only all uppercase TAGs will be valid
     	     String valid_level=validTags.get(gTag);
     	     if (valid_level!=null)
	     {
		     // if the read in level is the same as the level in the HashMap - then is valid
		     if (gLevel.equals(valid_level))
		     	validTag="Y";
	     }
	     else
     	     {
		     // Look to see if the third argurment in a valid TAG
		     // if the third item is one of the exception tags
		     // then switch the TAG and Arguments and check the level validity
     	             valid_level=validExTags.get(gArg);
		     if (valid_level!=null)
                     {
			// get the valid level for these TAGs, don't need to check for null 
			// since they are valid tags
			if (gLevel.equals(valid_level))
				validTag="Y";
			
			// switch the argument and tag values if is INDI or FAM
		        String tmp = gArg;
		        gArg = gTag;
		        gTag=tmp;
		     }
	     }
	 }
     }
     
     // Constructors
     /** constructor: object for parsing a GemDoc file */
     public GemDoc() {
	  
	  // Initialize the validTags hashMap
	  validTags=new HashMap<>();
	  validTags.put("NAME", "1");
	  validTags.put("SEX", "1");
	  validTags.put("BIRT", "1");
	  validTags.put("DEAT", "1");
	  validTags.put("FAMC", "1");
	  validTags.put("FAMS", "1");
	  validTags.put("MARR", "1");
	  validTags.put("HUSB", "1");
	  validTags.put("WIFE", "1");
	  validTags.put("CHIL", "1");
	  validTags.put("DIV", "1");
	  validTags.put("DATE", "2");
	  validTags.put("HEAD", "0");
	  validTags.put("TRLR", "0");
	  validTags.put("NOTE", "0");

	  // Initialize the validExTags hashMap
	  validExTags=new HashMap<>();
	  validExTags.put("FAM", "0");
	  validExTags.put("INDI", "0");
     }
     
     // methods
     /** parse_file parses the input file line by line
         @param filename input filename
         @return none
      */
     //public void parse_file(String filename) {
     public void parse_file(String filename) {

	FileInputStream fs; 
	try {

	     // open file name for reading
	     fs = new FileInputStream(filename);
	     Scanner sc=new Scanner(fs);

	     // read each line in the file - don't need to store line info yet - so just print out standard out
	     while (sc.hasNextLine()){
		     String line = sc.nextLine();

		     // declare object for processing the single line
                     GemDocLine gd_line = new GemDocLine(line);
		     gd_line.parse_line();
		     System.out.println("--> "+line);
		     System.out.println("<-- "+gd_line.get_level()+"|"+gd_line.get_tag()+"|"+gd_line.get_validity()+"|"+gd_line.get_args());
	     }
	     sc.close();
        }
	catch (IOException e) {
             // catch any IO exceptions
	     System.out.println("Problem reading file: "+filename);
	     e.printStackTrace();
	}

     }
     
    /** The main program reads in an input filename and prints out the output translation
        @param args arguments
    */
    public static void main(String args[]){
        // if an argument is passed on the command line - then process it
	// otherwise ask for file input.
	String filename="";

	if (args.length>0)
	{
		// check for arguments - basically just check the first argument and treat it
		// as the filename unless it is "--help"
		String arg1 =args[0];
		switch (arg1)
		{
			case "--help":
		             System.out.println("Valid Inputs: GEMDoc input Filename to be read");
			     System.exit(0);
			     break;

		        default:
	                     filename=arg1;
			     break;
	        }
	}
	else
	{
		// If a filename was not passed - ask the user for the filename
		Scanner sc = new Scanner (System.in);
		System.out.println("Input file name to read from: ");
		filename=sc.nextLine();
	}

        if (filename==null || filename.length()<1)
               throw new IllegalArgumentException("Filename must be at least one character");

	// Declare the GemDoc object for processing the input file
        GemDoc gd=new GemDoc();
	gd.parse_file(filename);
    }
}
