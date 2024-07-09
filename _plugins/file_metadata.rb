require 'pathname'
require 'zip'

module Jekyll
  class FileMetadataGenerator < Generator
    safe true

    # Constants for size units and threshold
    KB_THRESHOLD = 1024  # Threshold in KB to switch to MB

    SHAPEFILE_EXTENSIONS = %w[shp shx dbf prj sbn sbx fbn fbx ain aih ixs mxs atx shp.xml cpg qix].freeze

    def generate(site)
      site.pages.each do |page|
        next unless page.data['files']

        page.data['files'].each do |file|
          path = File.join(site.source, file['path'].sub(/^\//, ''))
          if File.exist?(path)
            file_size = File.size(path)
            if file_size >= KB_THRESHOLD * 1024
              file['size'] = (file_size / (1024 * 1024)).round # size in MB, rounded
              file['size_unit'] = 'MB'
            else
              file['size'] = (file_size / 1024).round # size in KB, rounded
              file['size_unit'] = 'KB'
            end

            if Pathname.new(path).extname == '.zip'
              file['format'] = detect_zip_contents(path)
            else
              file['format'] = Pathname.new(path).extname.sub('.', '').upcase
            end
          else
            Jekyll.logger.warn "File not found:", path
          end
        end
      end
    end

    def detect_zip_contents(zip_path)
      formats = []
      Zip::File.open(zip_path) do |zip_file|
        zip_file.each do |entry|
          next if entry.name == 'metadata.txt' # Ignore metadata.txt
          
          ext = Pathname.new(entry.name).extname.sub('.', '').downcase
          if SHAPEFILE_EXTENSIONS.include?(ext)
            formats << 'Shapefile'
          else
            formats << ext.upcase unless ext.empty?
          end
        end
      end
      formats.uniq!
      formats.delete('TXT') # Remove any 'TXT' formats as they're metadata files
      formats.join(', ')
    end
  end
end
