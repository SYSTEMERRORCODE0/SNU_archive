
public class Node<E> {

	private E item = null;
	private Node<E> right = null;
	private Node<E> left = null;

	public Node(E newItem, Node<E> left, Node<E> right) {
		this.item = newItem;
		this.left = left;
		this.right = right;
	}

	public Node<E> getLeft() {
		return this.left;
	}
	public Node<E> getRight() {
		return this.right;
	}

	public E getItem() {
		return this.item;
	}

	public void setLeft(Node<E> left) {
		this.left = left;
	}
	public void setRight(Node<E> right) {
		this.right = right;
	}

	public void setItem(E item) {
		this.item = item;
	}
}
