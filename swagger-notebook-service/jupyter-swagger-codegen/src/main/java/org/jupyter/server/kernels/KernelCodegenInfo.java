package org.jupyter.server.kernels;

public interface KernelCodegenInfo {
    /**
     * Supplies the string representing the symbols to start a single line comment in the language of the kernel.
     * @return A string representing the beginning of a single line comment
     */
    String getLanguageComment();

    /**
     * The name of the kernel to define in the notebook json. This should be
     * the value used to define the kernel.json for your kernel.
     * @return The name of the kernel
     */
    String getName();

    /**
     * The display name of the kernel within the Jupyter Notebook
     * @return A display name of the kernel
     */
    String getDisplayName();

    /**
     * The language of the code executed within the kernel
     * @return The language of the code executed within the kernel
     */
    String getLanguage();

}
