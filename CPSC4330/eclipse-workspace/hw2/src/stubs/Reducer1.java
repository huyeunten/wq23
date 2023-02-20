package stubs;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class Reducer1 extends Reducer<Text, Text, UserPairWritable, Text> {

  @Override
  public void reduce(Text key, Iterable<Text> values, Context context)
      throws IOException, InterruptedException {
	  
	  ArrayList<String> valueList = new ArrayList<>();
	  for (Text v : values) {
		  valueList.add(v.toString());
	  }
	  
	  List<String> unique = valueList.stream().distinct().collect(Collectors.toList());
	  
	  for (int i = 0; i < unique.size(); i++) {
		  for (int j = i + 1; j < unique.size(); j++) {
			  String user1 = unique.get(i);
			  String user2 = unique.get(j);
			  context.write(new UserPairWritable(user1, user2), key);
		  }
	  } 
  }
}