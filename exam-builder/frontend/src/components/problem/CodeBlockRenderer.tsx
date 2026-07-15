import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import { parsePlaceholders, parseCodeParts } from '../../ln/problem/l0/parsePlaceholders'

interface Props {
  content: string
  language?: string
}

function highlightCode(code: string, language?: string) {
  const { segments, blanks } = parsePlaceholders(code)

  let tokenized = ''
  for (let i = 0; i < segments.length; i++) {
    tokenized += segments[i]
    if (i < blanks.length) {
      tokenized += `__BLANK_${i}__`
    }
  }

  let highlighted: string
  if (language && hljs.getLanguage(language)) {
    highlighted = hljs.highlight(tokenized, { language }).value
  } else {
    highlighted = hljs.highlightAuto(tokenized).value
  }

  for (let i = 0; i < blanks.length; i++) {
    const label = blanks[i].label
    const escaped = label
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
    const cls = label ? 'placeholder-blank placeholder-labeled' : 'placeholder-blank'
    const content = escaped || '&nbsp;'
    highlighted = highlighted.replace(
      `__BLANK_${i}__`,
      `<span class="${cls}">${content}</span>`
    )
  }

  return highlighted
}

export function CodeBlockRenderer({ content, language }: Props) {
  const parts = parseCodeParts(content)
  const rows: JSX.Element[] = []
  let lineNumber = 1

  for (let pi = 0; pi < parts.length; pi++) {
    const part = parts[pi]
    if (part.type === 'code') {
      const highlighted = highlightCode(part.content, language)
      const lines = highlighted.split('\n')
      if (lines.length > 1 && lines[lines.length - 1] === '') {
        lines.pop()
      }
      for (let i = 0; i < lines.length; i++) {
        rows.push(
          <tr key={`${pi}-${i}`}>
            <td className="code-line-number">{lineNumber + i}</td>
            <td
              className="code-line-content"
              dangerouslySetInnerHTML={{ __html: lines[i] || ' ' }}
            />
          </tr>
        )
      }
      lineNumber += lines.length
    } else {
      const n = part.lines
      for (let i = 0; i < n; i++) {
        if (i === 0) {
          rows.push(
            <tr key={`blank-${pi}-${i}`}>
              <td className="code-line-number code-blank-number">{lineNumber + i}</td>
              <td className="code-block-blank-cell" rowSpan={n}>
                {Array.from({ length: n }, (_, j) => (
                  <div key={j} className="code-block-blank-line" />
                ))}
              </td>
            </tr>
          )
        } else {
          rows.push(
            <tr key={`blank-${pi}-${i}`}>
              <td className="code-line-number code-blank-number">{lineNumber + i}</td>
            </tr>
          )
        }
      }
      lineNumber += n
    }
  }

  return (
    <div className="code-block-wrapper">
      <table className="code-table">
        <tbody>{rows}</tbody>
      </table>
    </div>
  )
}
