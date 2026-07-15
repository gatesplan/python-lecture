import { parsePlaceholders } from '../../ln/problem/l0/parsePlaceholders'

interface Props {
  text: string
}

export function PlaceholderText({ text }: Props) {
  const { segments, blanks } = parsePlaceholders(text)

  if (blanks.length === 0) {
    return <>{text}</>
  }

  const parts: React.ReactNode[] = []
  for (let i = 0; i < segments.length; i++) {
    if (segments[i]) {
      parts.push(<span key={`s${i}`}>{segments[i]}</span>)
    }
    if (i < blanks.length) {
      const label = blanks[i].label
      parts.push(
        <span key={`b${i}`} className={label ? 'placeholder-blank placeholder-labeled' : 'placeholder-blank'}>
          {label || '\u00A0'}
        </span>
      )
    }
  }

  return <>{parts}</>
}
