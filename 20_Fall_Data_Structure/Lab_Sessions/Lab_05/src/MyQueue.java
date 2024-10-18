
public class MyQueue<E> implements Queue<E> {

	private Node<E> first = null;
	private Node<E> last = null;
	private int size = 0;

	@Override
	public void enqueue(E item) {
		// TODO Auto-generated method stub
		Node<E> temp = new Node<>(item, last, null);
		if(size == 0) first = temp;
		else last.setRight(temp);
		last = temp;
		size++;
	}

	@Override
	public E dequeue() {
		// TODO Auto-generated method stub
		if(size == 0) return null;
		E item = first.getItem();
		first = first.getRight();
		if(size == 1) {
			first = null;
			last = null;
		} else first.setLeft(null);
		size--;
		return item;
	}

	@Override
	public E pop() {
		// TODO Auto-generated method stub
		if(size == 0) return null;
		E item = last.getItem();
		last = last.getLeft();
		if(size == 1) {
			first = null;
			last = null;
		} else last.setRight(null);
		size--;
		return item;
	}

	@Override
	public void clear() {
		last = last.getRight();
		first = last;
		size = 0;
	}

	@Override
	public int size() {
		return this.size;
	}

	public boolean isEmpty() {
		return first == null;
	}

	public String toString() {
		Node<E> cursor = first;
		StringBuffer sb = new StringBuffer("(");
		while (cursor != null) {
			sb.append(cursor.getItem());
			if (cursor != last) {
				sb.append(' ');
			}
			cursor = cursor.getRight();
		}
		sb.append(")");
		return sb.toString();
	}

}
