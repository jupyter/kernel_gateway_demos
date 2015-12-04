package org.jupyter.server.kernels;

public class SparkKernelCodegen implements KernelCodegenInfo {
    @Override
    public String getLanguageComment() {
        return "//";
    }

    @Override
    public String getName() {
        return "spark";
    }

    @Override
    public String getDisplayName() {
        return "Spark Kernel (Scala)";
    }

    @Override
    public String getLanguage() {
        return "scala";
    }
}
