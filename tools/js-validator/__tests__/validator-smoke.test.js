const { NFOValidator } = require('../lib/validator');

describe('NFOValidator', () => {
  it('exports a validator class', () => {
    expect(typeof NFOValidator).toBe('function');
    const instance = new NFOValidator();
    expect(typeof instance.validateFile).toBe('function');
    expect(typeof instance.validateString).toBe('function');
  });
});
