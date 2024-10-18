#include <linux/debugfs.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/uaccess.h>
#include <asm/pgtable.h>
#define PTE_MASK 0xFFFFFFFFF000
#define PTE_SIGBIT_MASK 0x1FF
MODULE_LICENSE("GPL");

static struct dentry *dir, *output;
static struct task_struct *task;

static ssize_t read_output(struct file *fp,
                        char __user *user_buffer,
                        size_t length,
                        loff_t *position)
{
        // Implement read file operation
        // data type of struct packet
        struct packet {
        	pid_t pid;
        	unsigned long vaddr;
        	unsigned long paddr;
        };
        
        struct packet *pac = (struct packet*) user_buffer;
        
        /*
         *  In this architecture, VA is 64 bit but only use 48 bits for VPN
         *  [======16======][================36================][====12====]
         *      Not-Used                     VPN                     VPO    
         *                  [===9===][===9===][===9===][===9===][====12====]
         *                     PGD      PUD      PMD      PTE        VPO
         */
        pgd_t *pgd;
        pud_t *pud;
        pmd_t *pmd;
        pte_t *pte;
         
        unsigned long vpn = ((pac->vaddr) >> 12) & 0xFFFFFFFFF; // erase upper 16 bits & VPO
        unsigned long vpo = (pac->vaddr) & 0xFFF;
        unsigned long vpn_i[4];
        
        vpn_i[0] = vpn >> 27;
        vpn_i[1] = (vpn >> 18) & PTE_SIGBIT_MASK;
        vpn_i[2] = (vpn >> 9) & PTE_SIGBIT_MASK;
        vpn_i[3] = vpn & 0x1FF;
        
        task = pid_task(find_get_pid(pac->pid), PIDTYPE_PID);
        
        pgd = task->mm->pgd;
        pud = (pud_t *)(((pgd + vpn_i[0])->pgd & PTE_MASK) + PAGE_OFFSET);
        pmd = (pmd_t *)(((pud + vpn_i[1])->pud & PTE_MASK) + PAGE_OFFSET);
        pte = (pte_t *)(((pmd + vpn_i[2])->pmd & PTE_MASK) + PAGE_OFFSET);
        pac->paddr = (((pte + vpn_i[3])->pte & PTE_MASK) + vpo);
        
        return length;
}

static const struct file_operations dbfs_fops = {
        // Mapping file operations with your functions
        .read = read_output,
};

static int __init dbfs_module_init(void)
{
        // Implement init module

        dir = debugfs_create_dir("paddr", NULL);

        if (!dir) {
                printk("Cannot create paddr dir\n");
                return -1;
        }

        // Fill in the arguments below
        output = debugfs_create_file("output", S_IWUSR, dir, NULL, &dbfs_fops);
        
        printk("dbfs_paddr module initialize done\n");

        return 0;
}

static void __exit dbfs_module_exit(void)
{
        // Implement exit module
	debugfs_remove_recursive(dir);
	printk("dbfs_paddr module exit\n");
}

module_init(dbfs_module_init);
module_exit(dbfs_module_exit);
