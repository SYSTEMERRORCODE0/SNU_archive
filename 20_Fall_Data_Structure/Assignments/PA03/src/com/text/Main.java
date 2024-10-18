package com.text;

import com.sort.HybridSorter;
import com.sort.InsertionSorter;
import com.sort.Pair;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Array;

public class Main {

	// The main method below is optimized for huge input and output.
	// Please do not change the main method for the performance of your program.
	@SuppressWarnings("unchecked")
	public static void main(String[] args) throws IOException {
		final BufferedReader reader = new BufferedReader(new FileReader("testcase/input.txt"));
		
		// input
		int n1 = 0, n2 = 0, current = 0;
		Pair<String, Integer>[] array1 = null;
		Pair<String, Integer>[] array2 = null;
		//String[] array = new String[10000];
		String line = null;
		boolean sigle = true;
		
		// output
		final StringBuilder builder = new StringBuilder(512);
		
		// hybrid sorter
		final HybridSorter<String> sorter = new HybridSorter<String>();
		final InsertionSorter<String> insertionSorter = new InsertionSorter<String>();
		while ((line = reader.readLine()) != null) {
			final int index = line.indexOf(' ');
			String command = null;
			if (index == -1) {
				command = line;
			} else {
				command = line.substring(0, index);
			}
			if ("n".equals(command)) {
				final int secondIndex = line.indexOf(' ', index + 1);
				current = 0;
				if(secondIndex > 0){ // two arrays
					sigle = false;
					n1 = Integer.parseInt(line.substring(index + 1, secondIndex));
					n2 = Integer.parseInt(line.substring(secondIndex + 1));
					System.out.println("n1: " + n1 + " n2: " + n2);
					array1 = (Pair<String, Integer>[]) Array.newInstance(Pair.class, n1);
					array2 = (Pair<String, Integer>[]) Array.newInstance(Pair.class, n2);
				}else{
					sigle = true;
					n1 = Integer.parseInt(line.substring(index + 1));
					array1 = (Pair<String, Integer>[]) Array.newInstance(Pair.class, n1);
				}
			} else if ("append".equals(command)) {
				final int secondIndex = line.indexOf(' ', index + 1);
				final String key = line.substring(index + 1, secondIndex);
				final int value = Integer.parseInt(line.substring(secondIndex + 1));
				if(!sigle){
					array2[current] = new Pair<String, Integer>(key, value);
					++current;
					if(current == n2){ // last element of array2
						current = 0;
						sigle = true;
					}
				}else{
					array1[current] = new Pair<String, Integer>(key, value);
					//array[current] = key;
					++current;
				}

				System.out.println(key);
			} else if ("sort".equals(command)) {
				sorter.sort(array1, 0, array1.length - 1);
				System.out.println("Sorted");
			} else if ("search".equals(command)) {
				final int i = Integer.parseInt(line.substring(index + 1));
				Pair<String, Integer> search = (Pair<String, Integer>) sorter.search(array1, i);
				builder.append("Search: ");
				builder.append(i);
				builder.append(' ');
				builder.append(search.getKey());
				builder.append(' ');
				builder.append(search.getValue());
				System.out.println(builder.toString());
				builder.setLength(0);
			} else if ("median".equals(command)) {
				Pair<String, Integer> median = (Pair<String, Integer>) sorter.median(array1, array2);
				builder.append("Median: ");
				builder.append(median.getKey());
				builder.append(' ');
				builder.append(median.getValue());
				System.out.println(builder.toString());
				builder.setLength(0);
			} else if ("print".equals(command)) {
				final int i = Integer.parseInt(line.substring(index + 1));
				Pair<String, Integer> search = array1[i]; //(Pair<String, Integer>) sorter.search(array1, i);
				builder.append("Print: ");
				builder.append(i);
				builder.append(' ');
				builder.append(search.getKey());
				builder.append(' ');
				builder.append(search.getValue());
				System.out.println(builder.toString());
				builder.setLength(0);
			}
		}
		reader.close();
	}

}
