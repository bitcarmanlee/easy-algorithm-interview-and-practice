package edu.bit.carmanlee.datastruct.tree;

import java.util.Stack;

public class Traverse {

    public static void preorder(TreeNode root) {
        if (root == null) return;
        System.out.print(root.data + " ");
        preorder(root.left);
        preorder(root.right);
    }

    public static void preordernorecursive(TreeNode root) {
        if (root == null) return;
        Stack<TreeNode> stack = new Stack<>();
        stack.push(root);
        while (!stack.isEmpty()) {
            TreeNode tmp = stack.pop();
            System.out.print(tmp.data + " ");
            if (tmp.right != null) stack.push(tmp.right);
            if (tmp.left != null) stack.push(tmp.left);
        }
    }

    public static void inorder(TreeNode root) {
        if (root == null) return;
        inorder(root.left);
        System.out.print(root.data + " ");
        inorder(root.right);
    }

    public static void inorernorecursive(TreeNode root) {
        if (root == null) return;
        Stack<TreeNode> stack = new Stack<>();
        while (!stack.isEmpty() || root != null) {
            while (root != null) {
                stack.push(root);
                root = root.left;
            }
            if (!stack.isEmpty()) {
                root = stack.pop();
                System.out.print(root.data + " ");
                root = root.right;
            }
        }
    }

    public static void postorder(TreeNode root) {
        if (root == null) return;
        postorder(root.left);
        postorder(root.right);
        System.out.print(root.data + " ");
    }

    public static void postordernorecursive(TreeNode root) {
        if (root == null) return;
        Stack<TreeNode> stack = new Stack<>();
        TreeNode pre = root, cur = root;
        while (cur != null) {
            stack.push(cur);
            cur = cur.left;
        }

        while (! stack.isEmpty()) {
            cur = stack.pop();
            if (cur.right != null && cur.right != pre) {
                stack.push(cur);
                cur = cur.right;
                while (cur != null) {
                    stack.push(cur);
                    cur = cur.left;
                }
            } else {
                System.out.print(cur.data + " ");
                pre = cur;
            }
        }
    }

    public static void main(String[] args) {
        TreeNode root = TreeNodeInit.init();
        preorder(root);
        System.out.println();
        preordernorecursive(root);
        System.out.println();
        inorder(root);
        System.out.println();
        inorernorecursive(root);
        System.out.println();
        postorder(root);
        System.out.println();
        postordernorecursive(root);
    }
}
