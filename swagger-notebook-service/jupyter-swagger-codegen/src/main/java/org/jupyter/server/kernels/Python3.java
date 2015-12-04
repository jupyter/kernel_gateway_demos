package org.jupyter.server.kernels;

public class Python3 implements KernelCodegenInfo {
    @Override
    public String getLanguageComment() {
        return "#";
    }

    @Override
    public String getName() {
        return "python3";
    }

    @Override
    public String getDisplayName() {
        return "Python 3";
    }

    @Override
    public String getLanguage() {
        return "python";
    }
}
