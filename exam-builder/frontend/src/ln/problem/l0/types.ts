// ---------- Problem ----------

export interface Problem {
  type: ProblemType
  content: ContentBlock[]
  answer?: Answer
}

export type ProblemType =
  | 'select'   // 객관식
  | 'short'    // 단답형
  | 'explain'  // 서술형

// ---------- Content Blocks ----------

export type ContentBlock =
  | TextBlock
  | CodeBlock
  | ImageBlock
  | ParagraphBlock
  | TextChoicesBlock
  | ConditionBoxBlock
  | ItemBoxBlock
  | ProcessBoxBlock
  | InputSampleBlock
  | OutputSampleBlock
  | IoSampleBlock
  | AnswerBoxBlock

export interface TextBlock {
  type: 'text'
  content: string
  align?: 'left' | 'center' | 'right'
}

export interface CodeBlock {
  type: 'code'
  content: string
  language?: string
}

export interface ImageBlock {
  type: 'image'
  src: string     // public 경로(/images/x.png), 외부 URL, 또는 data URI
  alt?: string
  order?: number
  align?: 'left' | 'center' | 'right'
  width?: number  // mm
}

export interface ParagraphBlock {
  type: 'paragraph'
  blocks: (TextBlock | ImageBlock)[]
}

export interface TextChoicesBlock {
  type: 'text-choices'
  items: string[]
}

export type MarkerType = 'kr-con-rb' | 'kr-con' | 'en-cap' | 'en' | 'en-rb'

export const MARKERS: Record<MarkerType, string[]> = {
  'kr-con-rb': ['(ㄱ)', '(ㄴ)', '(ㄷ)', '(ㄹ)', '(ㅁ)', '(ㅂ)', '(ㅅ)', '(ㅇ)', '(ㅈ)', '(ㅊ)'],
  'kr-con': ['ㄱ.', 'ㄴ.', 'ㄷ.', 'ㄹ.', 'ㅁ.', 'ㅂ.', 'ㅅ.', 'ㅇ.', 'ㅈ.', 'ㅊ.'],
  'en-cap': ['A.', 'B.', 'C.', 'D.', 'E.', 'F.', 'G.', 'H.', 'I.', 'J.'],
  'en': ['a.', 'b.', 'c.', 'd.', 'e.', 'f.', 'g.', 'h.', 'i.', 'j.'],
  'en-rb': ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)', '(j)'],
}

export interface ConditionBoxBlock {
  type: 'condition-box'
  title?: string
  marker?: MarkerType
  items: string[]
}

export interface ItemBoxBlock {
  type: 'item-box'
  title?: string
  marker?: MarkerType
  items: (TextBlock | ImageBlock | ParagraphBlock)[]
}

export interface ProcessBoxBlock {
  type: 'process-box'
  title?: string
  content: ContentBlock[]
}

export interface InputSampleBlock {
  type: 'input-sample'
  content: string
}

export interface OutputSampleBlock {
  type: 'output-sample'
  content: string
}

export interface IoSampleBlock {
  type: 'io-sample'
  input: string
  output: string
}

export interface AnswerBoxBlock {
  type: 'answer-box'
  lines?: number  // default 6
}

// ---------- Answer ----------

export type Answer =
  | { type: 'choice'; value: number }
  | { type: 'value'; value: string }
