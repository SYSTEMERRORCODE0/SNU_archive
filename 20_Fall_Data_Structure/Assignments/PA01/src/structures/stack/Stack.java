package structures.stack;

public interface Stack<E> {
	/**
	 * Removes all of the elements in this stack.
	 */
	public void clear();

	/**
	 * Pushes an item onto the top of this stack.
	 * 
	 * @param item
	 *            the item to be pushed onto this stack
	 */
	public void push(E item);

	/**
	 * Removes the item at the top of this stack and returns that item as the
	 * value of this method.
	 * 
	 * @return the item at the top of this stack, or null if this stack is empty
	 */
	public E pop();

	/**
	 * Returns the number of elements in this stack.
	 * 
	 * @return the number of elements in this stack
	 */
	public int length();
	
	/**
	 * Returns true if this stack contains no elements.
	 * 
	 * @return true if this stack contains no elements
	 */
	public boolean isEmpty();
}
