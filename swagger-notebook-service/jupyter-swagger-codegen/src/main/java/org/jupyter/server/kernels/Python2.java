// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
package org.jupyter.server.kernels;

public class Python2 implements KernelCodegenInfo {
    @Override
    public String getLanguageComment() {
        return "#";
    }

    @Override
    public String getName() {
        return "python2";
    }

    @Override
    public String getDisplayName() {
        return "Python 2";
    }

    @Override
    public String getLanguage() {
        return "python";
    }
}
