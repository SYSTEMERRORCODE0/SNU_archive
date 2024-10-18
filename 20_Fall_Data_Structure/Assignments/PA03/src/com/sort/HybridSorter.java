package com.sort;


import java.lang.reflect.Array;

public class HybridSorter<K extends Comparable<? super K>> {
	InsertionSorter<K> insertionSort = new InsertionSorter<K>();
	QuickSorter<K> quickSort = new QuickSorter<K>();
	private final int RUN = 32;
	/**
	 * Sorts the elements in given array from `left` to `right in lexicographic order
	 * using the hybrid sorting algorithm.
	 */

	public Pair<K, ?> search(Pair<K,?>[] array, int k) {
		// Fill your code to find k-th element in `array`.
		Pair<K, ?>[] copyed = array.clone();
		sort(copyed, 0, copyed.length-1);
		return copyed[k-1];
	}
	
	public void sort(Pair<K, ?>[] array, int left, int right) {
		// Fill your code to sort the elements in `array`.
		quickSort.sort(array, left, right);			//roughly sort
		insertionSort.sort(array, left, right);		//perfectly sort after quickSort
	}

	public Pair<K, ?> median(Pair<K,?>[] array1, Pair<K,?>[] array2){
		// Fill your code to find median element
		// HINT: You might need to implement merge method that merges two sorted arrays
		int length;
		if(array2 != null) {
			length = array1.length + array2.length;
		} else {
			length = array1.length;
		}
		Pair<K, ?>[] copyed = (Pair<K, ?>[]) Array.newInstance(array1.getClass().getComponentType(), length);
		System.arraycopy(array1, 0, copyed, 0, array1.length);
		if(array2 != null) {
			System.arraycopy(array2, 0, copyed, array1.length, array2.length);
		}
		sort(copyed, 0, length - 1);
		if(length % 2 == 1) {
			return copyed[length/2];
		} else {
			Pair<K, String> pair = new Pair<>((K)(copyed[(length-1)/2].getKey() + "-" + copyed[length/2].getKey()),
											copyed[(length-1)/2].getValue() + "-" + copyed[length/2].getValue());
			return pair;
		}
	}
	
	public int min(int a, int b) {
		int res = 0;
		
		if (a > b ) res = b;
		else res = a;
		
		return res;
	}
	

}
