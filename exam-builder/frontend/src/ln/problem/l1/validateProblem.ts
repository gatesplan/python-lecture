import type { ContentBlock } from '../l0/types'

export interface ValidationResult {
  valid: boolean
  errors: string[]
}

const VALID_TYPES = new Set(['select', 'short', 'explain'])
const VALID_ANSWER_TYPES = new Set(['choice', 'value'])
const VALID_BLOCK_TYPES = new Set([
  'text', 'code', 'image', 'paragraph',
  'text-choices', 'condition-box', 'item-box', 'process-box',
  'input-sample', 'output-sample', 'io-sample', 'answer-box',
])

function validateBlock(block: any, path: string): string[] {
  const errors: string[] = []

  if (!block || typeof block !== 'object') {
    errors.push(`${path}: block is not an object`)
    return errors
  }

  if (!VALID_BLOCK_TYPES.has(block.type)) {
    errors.push(`${path}: unknown block type "${block.type}"`)
    return errors
  }

  switch (block.type) {
    case 'text':
      if (typeof block.content !== 'string') {
        errors.push(`${path}: text block requires string content`)
      }
      break

    case 'code':
      if (typeof block.content !== 'string') {
        errors.push(`${path}: code block requires string content`)
      }
      break

    case 'image':
      if (typeof block.src !== 'string' || block.src.length === 0) {
        errors.push(`${path}: image block requires non-empty src`)
      }
      break

    case 'text-choices':
      if (!Array.isArray(block.items) || block.items.length === 0) {
        errors.push(`${path}: text-choices requires non-empty items array`)
      }
      break

    case 'condition-box':
      if (!Array.isArray(block.items) || block.items.length === 0) {
        errors.push(`${path}: condition-box requires non-empty items array`)
      }
      break

    case 'item-box':
      if (!Array.isArray(block.items) || block.items.length === 0) {
        errors.push(`${path}: item-box requires non-empty items array`)
      }
      break

    case 'process-box':
      if (!Array.isArray(block.content) || block.content.length === 0) {
        errors.push(`${path}: process-box requires non-empty content array`)
      } else {
        for (let i = 0; i < block.content.length; i++) {
          errors.push(...validateBlock(block.content[i], `${path}.content[${i}]`))
        }
      }
      break

    case 'paragraph':
      if (!Array.isArray(block.blocks) || block.blocks.length === 0) {
        errors.push(`${path}: paragraph requires non-empty blocks array`)
      }
      break

    case 'input-sample':
      if (typeof block.content !== 'string') {
        errors.push(`${path}: input-sample requires string content`)
      }
      break

    case 'output-sample':
      if (typeof block.content !== 'string') {
        errors.push(`${path}: output-sample requires string content`)
      }
      break

    case 'io-sample':
      if (typeof block.input !== 'string') {
        errors.push(`${path}: io-sample requires string input`)
      }
      if (typeof block.output !== 'string') {
        errors.push(`${path}: io-sample requires string output`)
      }
      break
  }

  return errors
}

export function validateProblem(problem: any): ValidationResult {
  const errors: string[] = []

  if (!problem || typeof problem !== 'object') {
    return { valid: false, errors: ['problem is not an object'] }
  }

  if (!VALID_TYPES.has(problem.type)) {
    errors.push(`type: must be one of select, short, explain (got "${problem.type}")`)
  }

  if (!Array.isArray(problem.content) || problem.content.length === 0) {
    errors.push('content: must be a non-empty array')
  } else {
    for (let i = 0; i < problem.content.length; i++) {
      errors.push(...validateBlock(problem.content[i], `content[${i}]`))
    }
  }

  if (problem.answer !== undefined) {
    if (!problem.answer || typeof problem.answer !== 'object') {
      errors.push('answer: must be an object')
    } else if (!VALID_ANSWER_TYPES.has(problem.answer.type)) {
      errors.push(`answer: type must be choice or value (got "${problem.answer.type}")`)
    }
  }

  return { valid: errors.length === 0, errors }
}
