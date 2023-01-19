package stubs;
import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class ReviewMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

  @Override
  public void map(LongWritable key, Text value, Context context)
      throws IOException, InterruptedException {

	  // return key: product id, return value: rating
	  // add input validation
	  String line = value.toString();
	  
	  String[] all = line.split("\t");
	  
	  // check first line?
	  if (!all[7].equals("star_rating")) {		  
		  String id = all[3];
		  
		  int rating = Integer.parseInt(all[7]);
		  
		  context.write(new Text(id), new IntWritable(rating));
	  }
  }
}
