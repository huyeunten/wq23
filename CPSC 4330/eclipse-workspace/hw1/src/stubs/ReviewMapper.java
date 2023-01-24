package stubs;
import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class ReviewMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
  public boolean isNumber(String s) {
	  try {
		  Integer.parseInt(s);
		  return true;
	  } catch (NumberFormatException e) {
		  return false;
	  }
  }
	
  @Override
  public void map(LongWritable key, Text value, Context context)
      throws IOException, InterruptedException {

	  String line = value.toString();
	  
	  String[] all = line.split("\t");
	  
	  // make sure rating is a number
	  if (isNumber(all[7])) {		  
		  String id = all[3];
		  
		  int rating = Integer.parseInt(all[7]);
		  
		  context.write(new Text(id), new IntWritable(rating));
	  }
  }
}
