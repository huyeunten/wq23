package stubs;
import java.io.IOException;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class Mapper2 extends Mapper<LongWritable, Text, UserPairWritable, Text> {
  @Override
  public void map(LongWritable key, Text value, Context context)
      throws IOException, InterruptedException {
	  
	  String line = value.toString();
	  
	  String[] all = line.split("\t");
	  
	  if (all.length == 3) {
		  if (all[0].compareTo(all[1]) < 0)
			  context.write(new UserPairWritable(all[0], all[1]), new Text(all[2]));
		  else {
			  context.write(new UserPairWritable(all[1], all[0]), new Text(all[2]));
		  }
	  }
	}
}
