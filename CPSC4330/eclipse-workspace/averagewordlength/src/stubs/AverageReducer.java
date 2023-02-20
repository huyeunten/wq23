package stubs;
import java.io.IOException;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class AverageReducer extends Reducer<Text, IntWritable, Text, DoubleWritable> {

  @Override
  public void reduce(Text key, Iterable<IntWritable> values, Context context)
      throws IOException, InterruptedException {

    /*
     * TODO implement
     */
	  double total = 0;
	  int count = 0;
	  for (IntWritable length : values) {
		  total += length.get();
		  count++;
	  }
	  if (count != 0) {
		  double average = total / count;
		  
		  context.write(key, new DoubleWritable(average));  
	  }	  
  }
}