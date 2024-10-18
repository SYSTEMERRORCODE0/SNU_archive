import java.util.ArrayList;


public class BinarySearchTree<Key extends Comparable<? super Key>, E> {

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
         * replace the value of the node in the subtree.
         * Please compare keys using compareTo method.
         * e.g. when "int compare = KEY0.compareTo(KEY1)"
         * if compare == 0, this means KEY0 is equal to KEY1
         * if compare > 0, KEY0 > KEY1
         * if compare < 0, KEY0 < KEY1
         *
         * @param key
         * @param value
         * @return None
         */
        public void insert(Key key, E value) {
            int compare = mKey.compareTo(key);

            if (compare == 0) {
                mValue = value;
                return;
            } else if (compare > 0) {
                // mKey > key
                if (mLeft == null) {
                    mLeft = new Node(key, value);
                } else {
                    mLeft.insert(key, value);
                }
            } else {
                // mKey < key
                if (mRight == null) {
                    mRight = new Node(key, value);
                } else {
                    mRight.insert(key, value);
                }
            }
        }

        /**
         * Find the value of item by the key in the subtree, the root of which is this node.
         *
         * @param key
         * @return the value of item matched with the given key.
         * null, if there is no matching node in this subtree.
         */
        public E find(Key key) {
            int compare = mKey.compareTo(key);

            if (compare == 0) {
                return mValue;
            } else if (compare > 0) {
                // mKey > key
                if (mLeft == null) {
                    return null;
                } else {
                    return mLeft.find(key);
                }
            } else {
                // mKey < key
                if (mRight == null) {
                    return null;
                } else {
                    return mRight.find(key);
                }
            }

        }

        @Override
        public String toString() {
            return "[" + String.valueOf(mKey) + ":" + String.valueOf(mValue) + "]";
        }

        /**
         * Traverse with the preorder in this subtree.
         *
         * @return The String to be printed-out which contains series of nodes as the preorder traversal.
         */
        public String preorder() {
            String output = "";

            output += this.toString();
            if (mLeft != null)
                output += mLeft.preorder();
            if (mRight != null)
                output += mRight.preorder();
            return output;
        }

        /**
         * Traverse with the inorder in this subtree.
         *
         * @return The String to be printed-out which contains series of nodes as the inorder traversal.
         */
        public String inorder() {
            String output = "";

            if (mLeft != null)
                output += mLeft.inorder();
            output += this.toString();
            if (mRight != null)
                output += mRight.inorder();
            return output;

        }

        /**
         * Traverse with the postorder in this subtree.
         *
         * @return The String to be printed-out which contains series of nodes as the postorder traversal.
         */
        public String postorder() {
            String output = "";

            if (mLeft != null)
                output += mLeft.postorder();
            if (mRight != null)
                output += mRight.postorder();
            output += this.toString();
            return output;
        }

        /**
         * Find the height of this subtree
         *
         * @return height
         */
        public int height() {
            int height_left = (mLeft != null) ? mLeft.height() : 0;
            int height_right = (mRight != null) ? mRight.height() : 0;
            return Math.max(height_left, height_right) + 1;
        }

        public Node findMin() {
            if (mLeft == null)
                return this;
            else
                return mLeft.findMin();
        }

        /**
         * Delete a node,the key of which match with the key given as param, from this subtree.
         * You may need to define new method to find minimum of the subtree.
         *
         * @return the node of which parent needs to point after the deletion.
         */
        public Node delete(Key key) {
            int compare = mKey.compareTo(key);

            if (compare == 0) {
                if (mLeft != null && mRight != null) {
                    Node exchange = mRight.findMin();
                    mKey = exchange.getKey();
                    mValue = exchange.getValue();
                    mRight = mRight.delete(mKey);
                    return this;
                } else if (mLeft != null) {
                    return mLeft;
                } else {
                    return mRight;
                }
            } else if (compare > 0) {
                if (mLeft != null) {
                    mLeft = mLeft.delete(key);
                }
                return this;
            } else {
                if (mRight != null) {
                    mRight = mRight.delete(key);
                }
                return this;
            }
        }

        public int count() {
            return 1 + ((mLeft == null) ? 0 : mLeft.count()) + ((mRight == null) ? 0 : mRight.count());
        }

        public boolean isLeaf() {
            return (mLeft == null) && (mRight == null);
        }

        public int countLeafs() {
            if (isLeaf()) return 1;
            else return ((mLeft == null) ? 0 : mLeft.countLeafs()) + ((mRight == null) ? 0 : mRight.countLeafs());
        }

        /**
         * Get Lowest Common Ancester (LCA) of the given keys
         *
         * @param key1 the first given key
         * @param key2 the second given key
         * @return LCA
         */
        public Node getLCA(Key key1, Key key2) {
        	// TODO: Fill in this code
            if(key2.compareTo(key1) < 0) {  //swap to key1 <= key2
                Key temp = key2;
                key2 = key1;
                key1 = temp;
            }
            int keyCompare1 = mKey.compareTo(key1);
            int keyCompare2 = mKey.compareTo(key2);
            if(keyCompare1 == 0 && keyCompare2 == 0) return this;
            else if(keyCompare1 == 0) {
                if(find(key2) != null) return this;
                else return null;
            } else if(keyCompare2 == 0) {
                if(find(key1) != null) return this;
                else return null;
            }
            if(keyCompare1 > 0 && keyCompare2 > 0) {
                if(mLeft == null) return null;
                else return mLeft.getLCA(key1, key2);
            } else if(keyCompare1 < 0 && keyCompare2 < 0) {
                if(mRight == null) return null;
                else return mRight.getLCA(key1, key2);
            } else {
                if(find(key1) != null && find(key2) != null) return this;
                else return null;
            }
        }

        /**
         * Check if the tree is balanced or not
         *
         * @return check result
         */
        public boolean isBalanced() {
        	// TODO: Fill in this code
            if(mLeft == null && mRight == null) {
                return true;
            } else if(mLeft == null) {
                if(mRight.height() < 2) return true;
                return false;
            } else if(mRight == null) {
                if(mLeft.height() < 2) return true;
                return false;
            } else {
                if(Math.abs(mLeft.height() - mRight.height()) < 2) {
                    return mLeft.isBalanced() && mRight.isBalanced();
                } else {
                    return false;
                }
            }
        }

        /**
         * Extract nodes in the tree as a ArrayList of nodes.
         *
         * @return ArrayList of nodes
         */
        public ArrayList<Node> extractNodes() {
            // TODO: Fill in this code
            ArrayList<Node> arrayList = new ArrayList<>();
            if (mLeft != null)
                arrayList.addAll(mLeft.extractNodes());
            arrayList.add(this);
            if (mRight != null)
                arrayList.addAll(mRight.extractNodes());
            return arrayList;
        }
    }

    private Node mRoot;

    public BinarySearchTree() {
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

    public String preorder() {
        if (mRoot == null) {
            return null;
        }
        String res = mRoot.preorder();
        return res;
    }

    public String inorder() {
        if (mRoot == null) {
            return null;
        }
        String res = mRoot.inorder();
        return res;
    }

    public String postorder() {
        if (mRoot == null) {
            return null;
        }
        String res = mRoot.postorder();
        return res;
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

    public int countLeafs() {
        if (mRoot == null)
            return 0;
        return mRoot.countLeafs();
    }

    public Node getLCA(Key key1, Key key2) {
        return mRoot.getLCA(key1, key2);
    }

    public boolean isBalanced() {
        return mRoot.isBalanced();
    }

    /**
     * Recursive function for tree reconstruction
     *
     * @param nodes the ArrayList of nodes
     * @param low   the lowest index
     * @param high  the highest index
     * @param root  the root of the tree
     * @return fixed root of the tree
     */
    public Node recontructionHelp(ArrayList<Node> nodes, int low, int high, Node root) {
        //TODO: Fill in this code
        if(low > high) return null;
        int mid = (low + high) / 2;
        root = nodes.get(mid);
        root.mLeft = recontructionHelp(nodes, low, mid - 1, null);
        root.mRight = recontructionHelp(nodes, mid + 1, high, null);
        return root;
    }

    public void reconstruction() {
        ArrayList<Node> nodes = mRoot.extractNodes();
        if (nodes != null)
            mRoot = recontructionHelp(nodes, 0, nodes.size() - 1, null);
        else
            System.out.println("Check your implementation");
        System.out.println("reconstruction finished");
    }
}
