package structures.queue;

import java.util.LinkedList;

public class LinkedQueue<E> implements Queue<E> {
	
	private LinkedList<E> list = new LinkedList<E>();
	private E front = null;
	private E rear = null;
	private int length = 0;

	@Override
	public void clear() {
		//Fill your code here
		list.clear();
		front = null;
		rear = null;
		length = 0;
	}

	@Override
	public void enqueue(E item) {
		//Fill your code here
		list.add(item);
		if(front == null) front = item;
		rear = item;
		length++;
	}

	@Override
	public E dequeue() {
		//Fill your code here
		if(length == 0) {
			return null;
		}
		E e = list.removeFirst();
		if(length == 1) {
			front = null;
			rear = null;
		} else {
			front = list.getFirst();
		}
		length--;
		return e;
	}

	@Override
	public int length() {
		//Fill your code here
		return length;
	}

	@Override
	public boolean isEmpty() {
		//Fill your code here
		return list.isEmpty();
	}


}
