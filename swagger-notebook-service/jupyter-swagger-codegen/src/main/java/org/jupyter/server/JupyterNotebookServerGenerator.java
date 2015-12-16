// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
package org.jupyter.server;

import com.google.common.base.Joiner;
import com.google.common.base.Optional;
import com.google.common.collect.ImmutableMap;
import io.swagger.codegen.*;
import io.swagger.models.Operation;
import io.swagger.models.Swagger;
import org.jupyter.server.kernels.KernelCodegenInfo;
import io.swagger.codegen.CodegenConfig;
import java.io.File;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import static org.jupyter.server.JupyterCodegenContants.*;
import static org.jupyter.server.JupyterCodegenContants.CLIArgs.*;
import static org.jupyter.server.JupyterCodegenContants.Messages.*;

public class JupyterNotebookServerGenerator extends DefaultCodegen implements CodegenConfig {
  public JupyterNotebookServerGenerator() {
    super();
    outputFolder = DEFAULT_OUTPUT_DIR;
    templateDir = TEMPLATE_DIR;
    apiTemplateFiles.put(API_MUSTACHE, NOTEBOOK_FILE_EXTENSION);
    cliOptions.add(CLI_ARG_KERNEL);
  }
  
  @Override
  public CodegenType getTag() { return CodegenType.SERVER; }

  @Override
  public String getName() { return GENERATOR_NAME; }

  @Override
  public String getHelp() { return HELP_STRING; }
  
  @Override
  public void preprocessSwagger(Swagger swagger) {
    super.preprocessSwagger(swagger);
    additionalProperties.putAll(_getAdditionalProps(swagger, _getKernel()));

    for(Map.Entry<String, String> entry: SupportFiles.entrySet()) {
      supportingFiles.add(
          new SupportingFile(entry.getKey(), supportingFileDir(), entry.getValue())
      );  
    }
  }
  
  @Override
  public String apiFileFolder() {
    return Joiner.on(File.separator).skipNulls()
        .join(outputFolder, _getKernelName(), _getNotebookName(), SRC_DIR);
  }

  @Override
  public void addOperationToGroup(String tag, String resourcePath, Operation operation, CodegenOperation co, Map<String, List<CodegenOperation>> operations) {
    String baseResource = resourcePath;
    if (baseResource.startsWith(FORWARD_SLASH)) {
      baseResource = baseResource.substring(1);
    }
    int pos = baseResource.indexOf(FORWARD_SLASH);
    if (pos > 0) {
      baseResource = baseResource.substring(0, pos);
    }

    if (EMPTY_STRING.equals(baseResource)) {
      baseResource = DEFAULT;
    } else {
      if (co.path.startsWith(FORWARD_SLASH + baseResource)) {
        co.path = co.path.substring((FORWARD_SLASH + baseResource).length());
        co.path = _parameterizeURL(co.path);
      }
      co.subresourceOperation = !co.path.isEmpty();
    }
    co.baseName = baseResource;
    co.notes = _tidyString(co.notes);
    co.summary = _tidyString(co.summary);
    List<CodegenOperation> opsList =  Optional.
        fromNullable(operations.get(_getNotebookName())).
        or(new ArrayList<CodegenOperation>());
    
    opsList.add(co);
    operations.put(_getNotebookName(),opsList);
  }
  
  private String _tidyString(String value) {
    return EMPTY_STRING.equals(value)  ? null : value;
  }
  
  private KernelCodegenInfo _getKernel() {
    _validateKernelName(_getKernelName());
    return KernelCodegenImpls.get(_getKernelName());
  }
  
  private String _getNotebookName() {
    return Optional.of(additionalProperties.get(NOTEBOOK_NAME))
        .or(DEFAULT_NOTEBOOK_NAME).toString();
  }

  private String _getKernelName() {
    String name = Optional
        .of(additionalProperties.get(CLIArgs.CLI_ARG_KERNEL_ID))
        .or(DEFAULT_KERNEL_NAME).toString();
    return name;
  }

  private String supportingFileDir() {
    return String.format(SUPPORTING_FILES_DIR, _getKernelName(), _getNotebookName());
  }

  private void _validateKernelName(String name) {
    if(!KernelCodegenImpls.containsKey(name)) {
      System.err.println(String.format(KERNEL_NOT_SUPPORTED, name));
      System.err.println(SUPPORT_KERNELS_LIST);
      System.exit(1);
    }
  }

  private static Map<String, Object> _getAdditionalProps(Swagger swagger, KernelCodegenInfo kernel){
    String titleWithHyphens = swagger.getInfo().getTitle()
        .replaceAll(SPACE, HYPHEN);
    String titleNoSpaces = titleWithHyphens.replaceAll(HYPHEN, EMPTY_STRING);
    return ImmutableMap.<String,Object>builder().
      put(NOTEBOOK_NAME, titleNoSpaces).
      put(NOTEBOOK_FILE, titleNoSpaces + API_NOTEBOOK_EXTENSION).
      put(IMAGE_NAME, titleWithHyphens.toLowerCase()).
      put(KERNEL_DISPLAY_NAME, kernel.getDisplayName()).
      put(KERNEL_LANGUAGE, kernel.getLanguage()).
      put(KERNEL_NAME, kernel.getName()).
      put(KERNEL_LANG_COMMENT, kernel.getLanguageComment())
      .build();
  }

  private String _parameterizeURL(String path){
    Matcher matcher = Pattern.compile("\\{([^}]+)\\}").matcher(path);
    int start = 0;
    StringBuffer buf = new StringBuffer();
    while (matcher.find()) {
      buf.append(path.substring(start, matcher.start()));
      buf.append(COLON);
      buf.append(matcher.group(1));
      start = matcher.end();
    }
    buf.append(path.substring(start, path.length()));
    return buf.toString();
  }
}