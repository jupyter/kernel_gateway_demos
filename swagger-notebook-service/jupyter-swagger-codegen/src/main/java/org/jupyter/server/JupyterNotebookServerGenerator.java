package org.jupyter.server;

import io.swagger.codegen.*;
import io.swagger.models.Operation;
import org.jupyter.server.kernels.KernelCodegenInfo;
import io.swagger.codegen.CodegenConfig;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class JupyterNotebookServerGenerator extends DefaultCodegen implements CodegenConfig {
  protected String sourceFolder = "src";
  protected String kernelName = "python3";
  protected Map<String, KernelCodegenInfo> kernelMap = new HashMap<String, KernelCodegenInfo>();

  public CodegenType getTag() {
    return CodegenType.SERVER;
  }

  public String getName() {
    return "jupyter";
  }

  public String getHelp() {
    return "Generates a jupyter notebook with comments for turning the notebook into a REST API implementation. For more info see: https://github.com/jupyter-incubator/kernel_gateway";
  }

  public JupyterNotebookServerGenerator() {
    super();
    outputFolder = "target/swagger";
    apiTemplateFiles.put("api.mustache", ".ipynb");
    templateDir = "jupyter-swagger-codegen";

    ServiceLoader<KernelCodegenInfo> loader = ServiceLoader.load(KernelCodegenInfo.class);
    for (KernelCodegenInfo kernelInfo :loader) {
      kernelMap.put(kernelInfo.getName(), kernelInfo);
    }
    cliOptions.add(new CliOption("kernel", "The name of the kernel which will back the notebook."));
  }
  
  @Override
  public void processOpts() {
    super.processOpts();
    if (additionalProperties.containsKey("kernel")) {
      kernelName = (String) additionalProperties.get("kernel");
    }

    validateKernelName(kernelName);


    System.out.println("kernel is: " + kernelName);
    KernelCodegenInfo kernel = kernelMap.get(kernelName);
    additionalProperties.put("kernelDisplayName", kernel.getDisplayName());
    additionalProperties.put("kernelLanguage", kernel.getLanguage());
    additionalProperties.put("kernelName", kernel.getName());
    additionalProperties.put("kernelLangComment", kernel.getLanguageComment());
  }
  
  @Override
  public String apiFileFolder() {
    return outputFolder + "/" + kernelName + "/" + sourceFolder;
  }
  
  @Override
  public void addOperationToGroup(String tag, String resourcePath, Operation operation, CodegenOperation co, Map<String, List<CodegenOperation>> operations) {
    String baseResource = resourcePath;
    if (baseResource.startsWith("/")) {
      baseResource = baseResource.substring(1);
    }
    int pos = baseResource.indexOf("/");
    if (pos > 0) {
      baseResource = baseResource.substring(0, pos);
    }

    if ("".equals(baseResource)) {
      baseResource = "default";
    } else {
      if (co.path.startsWith("/" + baseResource)) {
        co.path = co.path.substring(("/" + baseResource).length());
        co.path = _parameterizeURL(co.path);
      }
      co.subresourceOperation = !co.path.isEmpty();
    }
    
    List<CodegenOperation> opList = operations.get(baseResource);
    if (opList == null) {
      opList = new ArrayList<>();
      operations.put(baseResource, opList);
    }
    opList.add(co);

    co.baseName = baseResource;
  }

  private void validateKernelName(String kernelName) {
    if(!kernelMap.containsKey(kernelName)) {
      System.err.println(String.format("Kernel %s is not supported.", kernelName));
      System.err.println("Supported kernels are: ");
      for(String kernel: kernelMap.keySet()) {
        System.err.println(String.format("\t%s", kernel));
      }
      System.exit(1);
    }
  }

  private String _parameterizeURL(String path){
    Matcher matcher = Pattern.compile("\\{([^}]+)\\}").matcher(path);
    int start = 0;
    StringBuffer buf = new StringBuffer();
    while (matcher.find()) {
      buf.append(path.substring(start, matcher.start()));
      buf.append(":");
      buf.append(matcher.group(1));
      start = matcher.end();
    }
    buf.append(path.substring(start, path.length()));
    return buf.toString();
  }
}