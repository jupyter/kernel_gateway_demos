package org.jupyter.server;

import com.google.common.collect.ImmutableMap;
import io.swagger.codegen.CliOption;
import org.jupyter.server.kernels.KernelCodegenInfo;
import java.util.HashMap;
import java.util.Map;
import java.util.ServiceLoader;

public class JupyterCodegenContants {
  //  Properties
  public static final String NOTEBOOK_NAME = "notebookName";
  public static final String NOTEBOOK_FILE = "notebookFile";
  public static final String IMAGE_NAME = "imageName";
  public static final String KERNEL_DISPLAY_NAME = "kernelDisplayName";
  public static final String KERNEL_LANGUAGE = "kernelLanguage";
  public static final String KERNEL_NAME = "kernelName";
  public static final String KERNEL_LANG_COMMENT = "kernelLangComment";
  
  //  Templates
  public static final String PACKAGE_MUSTACHE = "package.mustache";
  public static final String RUN_MUSTACHE = "run.mustache";
  public static final String DOCKERFILE_MUSTACHE = "Dockerfile.mustache";
  public static final String API_MUSTACHE = "api.mustache";
  
  //  Files
  public static final String DOCKERFILE = "Dockerfile";
  public static final String RUN_SH = "run.sh";
  public static final String PACKAGE_SH = "package.sh";
  public static final String NOTEBOOK_FILE_EXTENSION = ".ipynb";
  public static final String API_NOTEBOOK_EXTENSION = String.format("Api%s", NOTEBOOK_FILE_EXTENSION);

  //  Directories
  public static final String SUPPORTING_FILES_DIR = "%s/%s/src";
  public static final String DEFAULT_OUTPUT_DIR = "target/swagger";
  public static final String TEMPLATE_DIR = "jupyter-swagger-codegen";
  public static final String SRC_DIR = "src";
  
  //  Names
  public static final String GENERATOR_NAME = "jupyter";
  public static final String DEFAULT = "default";
  public static final String DEFAULT_KERNEL_NAME = "python3";
  public static final String DEFAULT_NOTEBOOK_NAME = "Default";
  
  //  Constant Characters
  public static final String COLON = ":";
  public static final String HYPHEN = "-";
  public static final String EMPTY_STRING = "";
  public static final String SPACE = " ";
  public static final String FORWARD_SLASH = "/";

  //  Command Line Arguments
  public static final class CLIArgs {
    public static final String CLI_ARG_KERNEL_ID = "kernel";
    public static final String CLI_ARG_KERNEL_DESCRIPTION = "The name of the kernel which will back the notebook.";
    public static final CliOption CLI_ARG_KERNEL = new CliOption(CLI_ARG_KERNEL_ID, CLI_ARG_KERNEL_DESCRIPTION);
  }
  
  public static final class Messages {
    public static final StringBuffer SUPPORT_KERNELS_LIST = new StringBuffer("Supported kernels are: ");
    public static final String KERNEL_NOT_SUPPORTED = "Kernel %s is not supported.";
    public static final String HELP_STRING = "Generates a jupyter notebook with comments for turning the notebook into a REST API implementation. For more info see: https://github.com/jupyter-incubator/kernel_gateway";
    
  }

  //  Support Files
  public static final Map<String, String> SupportFiles = ImmutableMap.<String,String>builder().
      put(PACKAGE_MUSTACHE, PACKAGE_SH).
      put(RUN_MUSTACHE, RUN_SH).
      put(DOCKERFILE_MUSTACHE, DOCKERFILE)
      .build();

  //  KernelCodegen Classes
  public static final Map<String, KernelCodegenInfo> KernelCodegenImpls = new HashMap<>();
  static {
    for(KernelCodegenInfo kernelCodegenInfo : ServiceLoader.load(KernelCodegenInfo.class)) {
      KernelCodegenImpls.put(kernelCodegenInfo.getName(), kernelCodegenInfo);
      Messages.SUPPORT_KERNELS_LIST.append(
          String.format("\t\t%s", kernelCodegenInfo.getName())
      );
    }
  }

}
