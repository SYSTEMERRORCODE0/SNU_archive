package com.sort;

import java.util.Random;

public class QuickSorter<K extends Comparable<? super K>>{
	public void sort(Pair<K, ?>[] array, int left, int right) {
		
		// Fill your code to sort the elements in `array`.
		int pivotindex = findpivot(array, left, right);
		swap(array, pivotindex, right);
		int pivot = partition(array, left-1, right, array[pivotindex].getKey());
		swap(array, pivot, right);
		if((pivot - left) > 31) sort(array, left, pivot-1);
		if((right - pivot) > 31) sort(array, pivot+1, right);
	}
	
	// Hint: Maybe you need to create helper methods.
	private void swap(Pair<K, ?>[] array, int a, int b) {
		Pair<K, ?> temp = array[a];
		array[a] = array[b];
		array[b] = temp;
	}

	private int partition(Pair<K, ?>[] array, int left, int right, K pivot) {
		do {
			while(array[++left].getKey().compareTo(pivot) < 0);
			while((right != 0) && array[--right].getKey().compareTo(pivot) > 0);
			swap(array, left, right);
		} while(left < right);
		swap(array, left, right);
		return left;
	}

	private int findpivot(Pair<K, ?>[] array, int left, int right) {
		Random random = new Random();
		int[] a = new int[3];
		for(int i = 0; i < 3; i++) {
			a[i] = random.nextInt(right-left) + left;
		}
		K k1 = array[a[0]].getKey();
		K k2 = array[a[1]].getKey();
		K k3 = array[a[2]].getKey();
		if(k1.compareTo(k2) <= 0 && k2.compareTo(k3) <= 0) return a[1];
		if(k2.compareTo(k3) <= 0 && k3.compareTo(k1) <= 0) return a[2];
		if(k3.compareTo(k1) <= 0 && k1.compareTo(k2) <= 0) return a[0];
		return a[1];
	}
}
