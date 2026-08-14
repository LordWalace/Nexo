export const logger = {
  info: (message: string, ...optionalParams: any[]) => {
    if (__DEV__) {
      console.log(message, ...optionalParams);
    }
  },
  warn: (message: string, ...optionalParams: any[]) => {
    if (__DEV__) {
      console.warn(message, ...optionalParams);
    }
  },
  error: (message: string, ...optionalParams: any[]) => {
    // Errors might be logged in production, but without sensitive data
    console.error(message, ...(__DEV__ ? optionalParams : []));
  },
  debug: (message: string, ...optionalParams: any[]) => {
    if (__DEV__) {
      console.debug(message, ...optionalParams);
    }
  }
};
