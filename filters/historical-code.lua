local function disclosure(block)
  for _, class_name in ipairs(block.classes) do
    if class_name == "equation-expression" then
      return block
    end
  end
  return {
    pandoc.RawBlock(
      "html",
      '<details class="historical-code-disclosure"><summary>Show historical code</summary>'
    ),
    block,
    pandoc.RawBlock("html", "</details>"),
  }
end

function Pandoc(doc)
  local execute = doc.meta.execute
  local enabled = execute and execute.enabled
  local historical = enabled ~= nil and pandoc.utils.stringify(enabled) == "false"
  if not historical then
    return doc
  end

  local walked = pandoc.walk_block(
    pandoc.Div(doc.blocks),
    { CodeBlock = disclosure }
  )
  doc.blocks = walked.content
  return doc
end
