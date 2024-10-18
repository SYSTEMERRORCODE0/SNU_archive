package structures.queue;

public interface Queue<E> {
	/**
	 * Removes all of the elements in this queue.
	 */
	public void clear();

	/**
	 * Inserts the specified element into this queue.
	 * 
	 * @param item
	 *            the element to add
	 */
	public void enqueue(E item);

	/**
	 * Retrieves and removes the head of this queue, or returns null if this
	 * queue is empty.
	 * 
	 * @return the head of this queue, or null if this queue is empty
	 */
	public E dequeue();

	/**
	 * Returns the number of elements in this queue.
	 * 
	 * @return the number of elements in this queue
	 */
	public int length();

	/**
	 * Returns true if this queue contains no elements.
	 * 
	 * @return true if this queue contains no elements
	 */
	public boolean isEmpty();

}
