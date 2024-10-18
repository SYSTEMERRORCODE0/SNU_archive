#include <linux/debugfs.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/uaccess.h>

MODULE_LICENSE("GPL");

static struct dentry *dir, *inputdir, *ptreedir;
static struct task_struct *curr;
static struct debugfs_blob_wrapper wrap;
static struct task_struct *parents[20000];
static char buf[100000];

static ssize_t write_pid_to_input(struct file *fp, 
                                const char __user *user_buffer, 
                                size_t length, 
                                loff_t *position)
{
        pid_t input_pid;
        int parents_length = 0;
        wrap.size = 0;

        sscanf(user_buffer, "%u", &input_pid);
        curr = pid_task(find_vpid(input_pid), PIDTYPE_PID); // Find task_struct using input_pid. Hint: pid_task

        // Tracing process tree from input_pid to init(1) process
        while(curr->pid != 1) {
        	parents[parents_length++] = curr;
        	curr = curr->real_parent;
        }
        parents[parents_length++] = curr;	// init (1), in my case systemmd (1)

        // Make Output Format string: process_command (process_id)
        parents_length--;
        while(parents_length >= 0) {
        	wrap.size += snprintf(wrap.data + wrap.size, 100000 - wrap.size, "%s (%d)\n", parents[parents_length]->comm, parents[parents_length]->pid);
        	parents_length--;
        }

        return length;
}

static const struct file_operations dbfs_fops = {
        .write = write_pid_to_input,
};

static int __init dbfs_module_init(void)
{
        // Implement init module code


        dir = debugfs_create_dir("ptree", NULL);
        
        if (!dir) {
                printk("Cannot create ptree dir\n");
                return -1;
        }

        inputdir = debugfs_create_file("input", S_IWUSR, dir, NULL, &dbfs_fops);
        ptreedir = debugfs_create_blob("ptree", S_IRUSR, dir, &wrap); // Find suitable debugfs API
        wrap.data = buf;
	
	
	printk("dbfs_ptree module initialize done\n");

        return 0;
}

static void __exit dbfs_module_exit(void)
{
        // Implement exit module code
	debugfs_remove_recursive(dir);
	printk("dbfs_ptree module exit\n");
}

module_init(dbfs_module_init);
module_exit(dbfs_module_exit);
