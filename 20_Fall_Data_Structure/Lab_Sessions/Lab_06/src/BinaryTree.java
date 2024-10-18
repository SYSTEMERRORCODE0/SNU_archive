public class BinaryTree<Key extends Comparable<? super Key>, E> {
	
	class Node {
		private Key mKey;
		private E mValue;

		private Node mLeft;
		private Node mRight;

		public Node(Key key, E value) {
			mKey = key;
			mValue = value;
			mLeft = null;
			mRight = null;
		}

		public Key getKey() {
			return mKey;
		}

		public E getValue() {
			return mValue;
		}

		/**
		 * Insert a node to the subtree, the root of which is this node.
		 * If the subtree already has node with the given key in the param,
		 * 		replace the value of the node in the subtree.
		 * Please compare keys using compareTo method.
		 * e.g. when "int compare = KEY0.compareTo(KEY1)"
		 * 		if compare == 0, this means KEY0 is equal to KEY1
		 * 		if compare > 0, KEY0 > KEY1
		 * 		if compare < 0, KEY0 < KEY1
		 * @param key
		 * @param value
		 * @return
		 * 			None
		 */
		public void insert(Key key, E value) {
			// TODO: Fill this function
			int compare = mKey.compareTo(key);
			if(compare == 0) {	//mKey == key
				mValue = value;
			} else if (compare < 0)	{	//mKey < key
				if(mRight == null) {
					mRight = new Node(key, value);
				} else {
					mRight.insert(key, value);
				}
			} else {
				if(mLeft == null) {
					mLeft = new Node(key, value);
				} else {
					mLeft.insert(key, value);
				}
			}
		}

		/**
		 * Find the value of item by the key in the subtree, the root of which is this node.
		 * @param key
		 * @return
		 * 			the value of item matched with the given key.
		 * 			null, if there is no matching node in this subtree.
		 */
		public E find(Key key) {
			// TODO: Fill this function
			int compare = mKey.compareTo(key);
			if(compare == 0) {	//mKey == key
				return mValue;
			} else if (compare < 0)	{	//mKey < key
				if(mRight == null) {
					return null;
				} else {
					return mRight.find(key);
				}
			} else {
				if(mLeft == null) {
					return null;
				} else {
					return mLeft.find(key);
				}
			}
		}

		@Override
		public String toString() {
			return "[" + String.valueOf(mKey) + ":" + String.valueOf(mValue) + "]";
		}

		/**
		 * Traverse with the preorder in this subtree.
		 * @return
		 * 			The String to be printed-out which contains series of nodes as the preorder traversal.
		 */
		public String preorder() {
			// TODO: Fill this function
			String output = "";
			output += toString();
			if(mLeft != null) output += mLeft.preorder();
			if(mRight != null) output += mRight.preorder();
			return output;
		}

		/**
		 * Traverse with the inorder in this subtree.
		 * @return
		 * 			The String to be printed-out which contains series of nodes as the inorder traversal.
		 */
		public String inorder() {
			// TODO: Fill this function
			String output = "";
			if(mLeft != null) output += mLeft.inorder();
			output += toString();
			if(mRight != null) output += mRight.inorder();
			return output;
		}

		/**
		 * Traverse with the postorder in this subtree.
		 * @return
		 * 			The String to be printed-out which contains series of nodes as the postorder traversal.
		 */
		public String postorder() {
			// TODO: Fill this function
			String output = "";
			if(mLeft != null) output += mLeft.postorder();
			if(mRight != null) output += mRight.postorder();
			output += toString();
			return output;
		}

		/**
		 * Find the height of this subtree
		 * @return
		 * 			height
		 */
		public int height() {
			// TODO: Fill this function
			if(mLeft == null && mRight == null) return 1;
			else if(mLeft == null) return mRight.height() + 1;
			else if(mRight == null) return mLeft.height() + 1;
			return Math.max(mLeft.height(), mRight.height()) + 1;
		}


		/**
		 * Delete a node,the key of which match with the key given as param, from this subtree.
		 * You may need to define new method to find minimum of the subtree.
		 * @return
		 * 			the node of which parent needs to point after the deletion.
		 */
		public Node delete(Key key) {
			// TODO: Fill this function
			int compare = mKey.compareTo(key);
			if(compare == 0) {	//mKey == key
				if(mLeft == null) return mRight;
				if(mRight == null) return mLeft;
				Node temp = mRight.getmin();
				mKey = temp.getKey();
				mValue = temp.getValue();
				mRight = mRight.delete(temp.getKey());
			} else if (compare < 0)	{	//mKey < key
				if(mRight != null) mRight = mRight.delete(key);
			} else {
				if(mLeft != null) mLeft = mLeft.delete(key);
			}
			return this;
		}

		public Node getmin() {
			if(mLeft == null) return this;
			return mLeft.getmin();
		}

		/**
		* Count the number of nodes in subtree
		* @return
		* 		the number of subnodes + current node
		* */
		public int count(){
			if(mLeft == null && mRight == null) return 1;
			else if(mLeft == null) return mRight.count() + 1;
			else if(mRight == null) return mLeft.count() + 1;
			return mRight.count() + mLeft.count() + 1;
		}

		/**
		 * Count the number of leaf nodes in the current subtree
		 * You may need to define a new method to find if current node is a leaf node
		 * @return
		 * 		the number of leaf nodes
		 * */
		public int countLeafs(){
			if(mLeft == null && mRight == null) return 1;
			else if(mLeft == null) return mRight.countLeafs();
			else if(mRight == null) return mLeft.countLeafs();
			return mRight.countLeafs() + mLeft.countLeafs();
		}

	}



	// Please do not touch rest of the code since it is related to the output format ----------------------------------------------
	private Node mRoot;
	public BinaryTree() {
		mRoot = null;
	}
	
	public void insert(Key key, E value) {
		if (mRoot == null) {
			mRoot = new Node(key, value);
		} else {
			mRoot.insert(key, value);
		}
	}
	
	public void delete(Key key) {
		if (mRoot == null)
			return;
		mRoot = mRoot.delete(key);
	}
	
	public E find(Key key) {
		if (mRoot == null)
			return null;
		return mRoot.find(key);
	}
	
	public void preorder() {
		System.out.print("preorder : ");
		if (mRoot == null) {
			System.out.println("None");
			return;
		}
		System.out.println(mRoot.preorder());
	}
	
	public void inorder() {
		System.out.print("inorder : ");
		if (mRoot == null) {
			System.out.println("None");
			return;
		}
		System.out.println(mRoot.inorder());
	}
	
	public void postorder() {
		System.out.print("postorder : ");
		if (mRoot == null) {
			System.out.println("None");
			return;
		}
		System.out.println(mRoot.postorder());
	}
	
	public int height() {
		if (mRoot == null)
			return 0;
		return mRoot.height();
	}

	public int count() {
		if (mRoot == null)
			return 0;
		return mRoot.count();
	}

	public int countLeafs(){
		if (mRoot == null)
			return 0;
		return mRoot.countLeafs();
	}
}
