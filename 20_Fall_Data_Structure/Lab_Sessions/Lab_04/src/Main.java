import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;
public class Main {
	public static void main(String[] args){
		SingleLinkedList<String> list = new SingleLinkedList<String>();

		String inputFilePath;
		if(System.getProperty("file.separator").equals("\\"))
			inputFilePath = Paths.get("testinput", "input.txt").toString();
		else
			inputFilePath = "testinput/input.txt";
		try {
			BufferedReader reader = new BufferedReader(new FileReader(inputFilePath));
			String line = null;
			System.out.println("Operate Value\tLinkedLists");
			System.out.println("---------------------");
			while ((line = reader.readLine()) != null) {
				System.out.print(line + "\n");
				if (line.startsWith("insert")) {
					int pos = Integer.parseInt(line.split(" ")[1]);
					String val = line.split(" ")[2];
					System.out.print("INSERT: ");
					list.insert(pos, val);
				} else if (line.startsWith("remove")) {
					int pos = Integer.parseInt(line.split(" ")[1]);
					System.out.print("REMOVE: ");
					list.remove(pos);
				} else if (line.startsWith("getValue")) {
					int pos = Integer.parseInt(line.split(" ")[1]);
					System.out.print("GET: ");
					String elem = list.getValue(pos);
					if (elem != null) {
						System.out.printf("%d, %s", pos, elem);
					} else {
						System.out.print("INVALID");
					}
				} else if (line.startsWith("update")) {
					int pos = Integer.parseInt(line.split(" ")[1]);
					String val = line.split(" ")[2];
					System.out.print("UPDATE: ");
					list.update(pos, val);
				} else if (line.startsWith("printAll")) {
					System.out.print("ALL: ");
					list.printAll();
				} else if (line.startsWith("length")) {
					int len = list.length();
					System.out.printf("LENGTH: %d", len);
				} else {
					System.out.println("Unknown command!");
					break;
				}
				System.out.println();
			}
		}catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
