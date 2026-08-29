local function enabled(meta)
  return meta["reading-time"] ~= nil and pandoc.utils.stringify(meta["reading-time"]) == "true"
end

function Pandoc(doc)
  if not FORMAT:match("html") or not enabled(doc.meta) then
    return doc
  end

  local words = 0
  local text = pandoc.utils.stringify(doc.blocks)
  for _ in text:gmatch("%S+") do
    words = words + 1
  end
  local minutes = math.max(1, math.ceil(words / 200))
  local line = pandoc.Para({pandoc.Str(tostring(minutes) .. " min read")})
  table.insert(doc.blocks, 1, pandoc.Div({line}, pandoc.Attr("", {"article-reading-time"})))
  return doc
end
