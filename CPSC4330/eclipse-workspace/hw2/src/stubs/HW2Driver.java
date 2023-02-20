package stubs;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.conf.Configuration;

public class HW2Driver {

  public static void main(String[] args) throws Exception {

    /*
     * Validate that three arguments were passed from the command line.
     */
    if (args.length != 3) {
      System.out.printf("Usage: HW2 <input dir> <temp output dir> <output dir\n");
      System.exit(-1);
    }

    /*
     * Instantiate a Job object for your job's configuration. 
     */
    Configuration conf = new Configuration();
    
    // Job 1
    Job job1 = Job.getInstance(conf, "job1");

    job1.setJarByClass(HW2Driver.class);
    
    FileInputFormat.setInputPaths(job1, new Path(args[0]));
    FileOutputFormat.setOutputPath(job1, new Path(args[1]));
    
    job1.setMapperClass(Mapper1.class);
    job1.setReducerClass(Reducer1.class);
    
    job1.setMapOutputKeyClass(Text.class);
    job1.setMapOutputValueClass(Text.class);
    
    job1.setOutputKeyClass(UserPairWritable.class);
    job1.setOutputValueClass(Text.class);

    int job1Complete = job1.waitForCompletion(true) ? 0 : 1;
    if (job1Complete != 0) {
    	System.out.println("Job 1 failed, exiting");
    	System.exit(1);
    }
    
    // Job 2
    Job job2 = Job.getInstance(conf, "job2");
    
    job2.setJarByClass(HW2Driver.class);
    
    FileInputFormat.setInputPaths(job2, new Path(args[1]));
    FileOutputFormat.setOutputPath(job2, new Path(args[2]));
    
    job2.setMapperClass(Mapper2.class);
    job2.setReducerClass(Reducer2.class);
    
    job2.setMapOutputKeyClass(UserPairWritable.class);
    job2.setMapOutputValueClass(Text.class);
    
    job2.setOutputKeyClass(UserPairWritable.class);
    job2.setOutputValueClass(Text.class);
    
    boolean success = job2.waitForCompletion(true);
    System.exit(success ? 0 : 1);
  }
}

