import { PlaceholderText } from './PlaceholderText'

interface Props {
  items: string[]
}

const CHOICE_MARKERS = [
  '\u2460', '\u2461', '\u2462', '\u2463', '\u2464',
  '\u2465', '\u2466', '\u2467', '\u2468', '\u2469',
]

export function TextChoicesRenderer({ items }: Props) {
  return (
    <div className="text-choices">
      {items.map((item, i) => (
        <span key={i} className="text-choice-item">
          <span className="choice-marker">
            {CHOICE_MARKERS[i] ?? `(${i + 1})`}
          </span>
          <PlaceholderText text={item} />
        </span>
      ))}
    </div>
  )
}
