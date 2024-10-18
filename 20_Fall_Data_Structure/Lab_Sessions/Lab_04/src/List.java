/**
 * This is an interface of List. Do not change this interface. 
 * @author SNU 2015 Fall Data Structure T.A.
 *
 */

/** List ADT */
public interface List<E> {
	public void insert(int pos, E item);
	public void remove(int pos);
	public int length();
	public E getValue(int pos);
	public void printAll(); // simply print all the elements inside
	public void update(int pos, E item);
}