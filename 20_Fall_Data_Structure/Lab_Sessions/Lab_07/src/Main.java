import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {

	@SuppressWarnings("resource")
	public static void main(String[] args) throws IOException {
		
		try {
			BinarySearchTree<Integer, String> bt = new BinarySearchTree<>();
			
			FileInputStream fis = new FileInputStream("sample_input.txt");
			BufferedReader reader = new BufferedReader(new InputStreamReader(fis));
			for (String line=reader.readLine(); line !=null; line=reader.readLine()) {
				String[] line_split = line.split(" ");
				String cmd = line_split[0];
				
				if (cmd.equals("insert")) {
					Integer key = Integer.parseInt(line_split[1]);
					String value = line_split[2];
					bt.insert(key, value);
				} else if (cmd.equals("delete")) {
					Integer key = Integer.parseInt(line_split[1]);
					bt.delete(key);
				} else if (cmd.equals("find")) {
					Integer key = Integer.parseInt(line_split[1]);
					System.out.println("Value for " + String.valueOf(key) + " is  " + bt.find(key));
				} else if (cmd.equals("preorder")) {
					System.out.print("preorder: ");
					String res = bt.preorder();
					if (res==null)
						System.out.println("None");
					else
						System.out.println(res);
				} else if (cmd.equals("inorder")) {
					System.out.print("inorder: ");
					String res = bt.inorder();
					if (res==null)
						System.out.println("None");
					else
						System.out.println(res);
				} else if (cmd.equals("postorder")) {
					System.out.print("postorder: ");
					String res = bt.postorder();
					if (res==null)
						System.out.println("None");
					else
						System.out.println(res);
				} else if (cmd.equals("height")) {
					System.out.println("Height of this tree is " + String.valueOf(bt.height()));
				} else if (cmd.equals("count")) {
					System.out.println("The total number of nodes is " + String.valueOf(bt.count()));
				} else if (cmd.equals("countLeafs")) {
					System.out.println("The total number of leaf nodes is " + String.valueOf(bt.countLeafs()));
				}
				else if (cmd.equals("reconstruction")){
					bt.reconstruction();
				}
				else if (cmd.equals("lca")){
					Integer key1 = Integer.parseInt(line_split[1]);
					Integer key2 = Integer.parseInt(line_split[2]);
					BinarySearchTree.Node res = bt.getLCA(key1, key2);
					if (res == null)
						System.out.println("There is an unknown key");
					else
						System.out.println("lca of " + key1 + ", " + key2 + ": " + bt.getLCA(key1, key2));
				}
				else if (cmd.equals("balanceCheck")){
					boolean res = bt.isBalanced();
					if (res)
						System.out.println("The tree is balanced");
					else
						System.out.println("The tree is not balanced");
				}

			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
