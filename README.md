# PDF viewer

A simple PDF viewer that returns a stored PDF in a S3 bucket, deployed as AWS Gateway API with Lambda proxy integration

PDF id must exist on database, otherwise 404 will be returned. The file name, however, is ignored, but sent back as <code>Content-Disposition</code> header

API Gateway endpoint [example](https://pdf.livestory.io/viewer/6834895dc979d45ef5bd047d/Dummy%20PDF%20file.pdf)

## PDF Download option
By simply using <code>download</code> action in path: [https://pdf.livestory.io/download/6834895dc979d45ef5bd047d/Dummy%20PDF%20file.pdf](https://pdf.livestory.io/download/6834895dc979d45ef5bd047d/Dummy%20PDF%20file.pdf)
