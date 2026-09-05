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
  table.insert(doc.blocks, 2, pandoc.RawBlock("html", [[
<script>
(() => {
  const reading = document.querySelector('.article-reading-time');
  const published = document.querySelector('#title-block-header .quarto-title-meta-contents .date');
  if (!reading || !published) return;
  const inline = document.createElement('span');
  inline.className = 'article-reading-time-inline';
  inline.textContent = ` · ${reading.textContent.trim()}`;
  published.append(inline);
  reading.remove();
})();
</script>
]]))
  return doc
end
