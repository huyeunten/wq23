package stubs;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class Reducer2 extends Reducer<UserPairWritable, Text, UserPairWritable, Text> {

  @Override
  public void reduce(UserPairWritable key, Iterable<Text> values, Context context)
      throws IOException, InterruptedException {
	  
	  ArrayList<String> valueList = new ArrayList<>();
	  for (Text v : values) {
		  valueList.add(v.toString());
	  }
	  
	  List<String> unique = valueList.stream().distinct().collect(Collectors.toList());
	
	  
	  if (unique.size() >= 3) {
		  String products = "";
		  for (int i = 0; i < unique.size(); i++) {
			  if (products.equals("")) {
				  products = unique.get(i);
			  }
			  else {
				  products = products + ", " + unique.get(i);
			  }
		  }
		  context.write(key, new Text(products));
	  }
  }
}