package stubs;
import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class AvgReducer extends Reducer<Text, IntWritable, Text, Text> {

  @Override
  public void reduce(Text key, Iterable<IntWritable> values, Context context)
      throws IOException, InterruptedException {

	  double total = 0;
	  int count = 0;
	  for (IntWritable length : values) {
		  total += length.get();
		  count++;
	  }
	  if (count != 0) {
		  double average = total / count;
		  
		  String rating = Integer.toString(count) + ", " + Double.toString(average);
		  
		  context.write(key, new Text(rating));  
	  }
	  else {
		  String zero = "0, 0";
		  context.write(key, new Text(zero));
	  }
  }
}