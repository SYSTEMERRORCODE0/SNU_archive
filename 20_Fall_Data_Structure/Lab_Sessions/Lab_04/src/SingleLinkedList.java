/** Source code example for "A Practical Introduction to Data
    Structures and Algorithm Analysis, 3rd Edition (Java)" 
    by Clifford A. Shaffer
    Copyright 2008-2011 by Clifford A. Shaffer
 */

/** Linked list implementation */
class SingleLinkedList<E> implements List<E> {
	private Link<E> head;         // Pointer to list header
	private Link<E> tail;         // Pointer to last element
	protected Link<E> curr;       // Access to current element
	int cnt = 0;		      // Size of list

	/** Constructors */
	SingleLinkedList(int size) { this(); }   // Constructor -- Ignore size
	SingleLinkedList() {
		curr = tail = head = new Link<E>(null);
	}

	/** Insert "it" at (pos) position */
	public void insert(int pos, E it) {
		// fill your code here
		if(pos>cnt+1) {
			System.out.print("INVALID");
		} else {
			Link<E> curr = head;
			for(int i=1; i<pos; i++) {
				curr = curr.next();
			}
			curr.setNext(new Link<E>(it, curr.next()));
			if(tail == curr) tail = curr.next();
			cnt++;
			System.out.print(pos + ", " + curr.next().element());
		}
	}

	/** Remove an element at (pos) position*/
	public void remove(int pos) {
		// fill your code here
		if(pos>cnt) {
			System.out.print("INVALID");
		} else {
			Link<E> curr = head;
			for(int i=1; i<pos; i++) {
				curr = curr.next();
			}
			System.out.print(pos + ", " + curr.next().element());
			if(curr.next() == tail) tail = curr;
			curr.setNext(curr.next().next());
			cnt--;
		}
	}

	/** @return an element value at (pos) position*/
	public E getValue(int pos) {
		// fill your code here
		if(pos>cnt) {
			return null;
		} else {
			Link<E> curr = head;
			for(int i=1; i<pos; i++) {
				curr = curr.next();
			}
			return curr.next().element();
		}
	}

	/** Print all the values in the list*/
	public void printAll() { // simply print all the elements inside
		// fill your code here
		Link<E> curr = head;
		while((curr = curr.next()) != null) {
			System.out.print(curr.element() + " ");
		}
	}
	/** Update element at (pos) position*/
	public void update(int pos, E item){
		// fill your code here
		if(pos>cnt) {
			System.out.print("INVALID");
		} else {
			Link<E> curr = head;
			for(int i=1; i<pos; i++) {
				curr = curr.next();
			}
			curr.next().setElement(item);
			System.out.print(pos + ", " + curr.next().element());
		}
	}
	/** @return List length */
	public int length() {
		// fill your code here
		return cnt;
	}
}