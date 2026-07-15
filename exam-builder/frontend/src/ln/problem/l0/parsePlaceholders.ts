export interface Blank {
  index: number
  label: string
}

export interface BlockBlank {
  lines: number
}

export interface ParseResult {
  segments: string[]
  blanks: Blank[]
}

export interface CodeSegment {
  type: 'code'
  content: string
}

export interface BlockBlankSegment {
  type: 'block-blank'
  lines: number
}

export type CodePart = CodeSegment | BlockBlankSegment

const PLACEHOLDER_RE = /\[\[(.*?)\]\]/g
const BLOCK_BLANK_RE = /^\[\[\[(\d*)\]\]\]$/

/**
 * 코드 문자열을 [[[N]]] 기준으로 분할한다.
 * [[[N]]]은 반드시 한 줄 전체를 차지해야 한다.
 */
export function parseCodeParts(input: string): CodePart[] {
  const lines = input.split('\n')
  const parts: CodePart[] = []
  let codeLines: string[] = []

  const flushCode = () => {
    if (codeLines.length > 0) {
      parts.push({ type: 'code', content: codeLines.join('\n') })
      codeLines = []
    }
  }

  for (const line of lines) {
    const match = BLOCK_BLANK_RE.exec(line.trim())
    if (match) {
      flushCode()
      const n = match[1] ? parseInt(match[1], 10) : 3
      parts.push({ type: 'block-blank', lines: n })
    } else {
      codeLines.push(line)
    }
  }
  flushCode()

  return parts
}

export function parsePlaceholders(input: string): ParseResult {
  const segments: string[] = []
  const blanks: Blank[] = []

  let lastIndex = 0
  let match: RegExpExecArray | null
  let blankIndex = 0

  while ((match = PLACEHOLDER_RE.exec(input)) !== null) {
    segments.push(input.slice(lastIndex, match.index))
    blanks.push({ index: blankIndex++, label: match[1] })
    lastIndex = match.index + match[0].length
  }

  segments.push(input.slice(lastIndex))
  return { segments, blanks }
}
